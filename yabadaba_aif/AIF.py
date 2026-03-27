from io import IOBase
from typing import Optional, Union
from yabadaba.record import Record

from DataModelDict import uber_open_rmode
from DataModelDict import DataModelDict as DM

from gemmi import cif

import numpy as np

class AIF(Record):

    """
    Class for managing input settings and building grain boundary
    configurations according to the GRIP algorithm.
    """

    def __init__(self,
                 model: Union[str, IOBase, DM, None] = None,
                 name: Optional[str] = None,
                 aif: Union[str, IOBase, None] = None,
                 database = None,
                 noname: bool = False,
                 **kwargs):
        """
        Initializes a Record object for a given style.
        
        Parameters
        ----------
        model : str, file-like object, or DataModelDict, optional
            The contents of the record.
        name : str, optional
            The unique name to assign to the record.  If model is a file
            path, then the default record name is the file name without
            extension.
        aif : str or file-like object, optional
            The contents of the record stored as an AIF file.
        database : yabadaba.Database, optional
            A default Database to associate with the Record, typically the
            Database that the Record was obtained from.  Can allow for Record
            methods to perform Database operations without needing to specify
            which Database to use.
        nonoame : bool, optional
            Flag indicating if the record does not get assigned a name.  This
            is primarily for when a record class is used as a value inside
            another class, i.e., this record is a subset of another.
        kwargs : any
            Any record-specific attributes to assign.
        """
        super().__init__(model=model, name=name, database=database, noname=noname, **kwargs)

        if aif is not None:
            if model is not None or name is not None or len(kwargs) > 0:
                raise ValueError('aif file cannot be given with model, name or kwargs')
            self.read_aif(aif)


    ########################## Basic metadata fields ##########################

    @property
    def style(self) -> str:
        """str: The record style"""
        return 'aif'

    @property
    def modelroot(self) -> str:
        """str: The root element of the content"""
        return 'aif'

    ####################### Define Values and attributes #######################

    def _init_values(self):
        """
        Method that defines the value objects for the Record.  This should
        call the super of this method, then use self._add_value to create new Value objects.
        Note that the order values are defined matters
        when build_model is called!!!
        """
        
        self._init_values_audit()
        self._init_values_exptl()
        self._init_values_adsnt()
        self._init_values_simltn()
        self._init_values_units()
        self._init_values_citation()
        self._init_values_desorp()
        self._init_values_adsorp()
        
    def _init_values_audit(self):
        """Initialize audit subset of values"""

        self._add_value('str', 'audit_aif_version',
                        modelpath='audit.aif_version',
                        description='version of AIF data names (Github commit hash)')
        
    def _init_values_exptl(self):
        """Initialize exptl subset of values"""
        
        self._add_value('str', 'exptl_adsorptive',
                        modelpath='exptl.adsorptive',
                        description='name of the adsorptive')
        self._add_value('str', 'exptl_adsorptive_name',
                        modelpath='exptl.adsorptive_name',
                        description='secondary identifier')
        self._add_value('str', 'exptl_date',
                        modelpath='exptl.date',
                        description='date of the experiment (string in ISO 8601 format)')
        self._add_value('str', 'exptl_digitizer',
                        modelpath='exptl.digitizer',
                        description='name of the person who digitized the experiment')
        self._add_value('str', 'exptl_instrument',
                        modelpath='exptl.instrument',
                        description='instrument id used for the experiment')
        self._add_value('str', 'exptl_isotherm_type',
                        modelpath='exptl.isotherm_type',
                        description='description of isotherm type, eg. absolute, excess, net')
        self._add_value('str', 'exptl_method',
                        modelpath='exptl.method',
                        description='description of method used to determine amount adsorbed, eg. volumetric')
        self._add_value('str', 'exptl_operator',
                        modelpath='exptl.operator',
                        description='name of the person who ran the experiment')
        self._add_value('float', 'exptl_p0',
                        modelpath='exptl.p0',
                        description='saturation pressure of the experiment at the temperature of the experiment')
        self._add_value('float', 'exptl_p0_uncertainty',
                        modelpath='exptl.p0_uncertainty',
                        description='saturation pressure of the experiment at the temperature of the experiment uncertainty')
        self._add_value('float', 'exptl_temperature',
                        modelpath='exptl.temperature',
                        description='temperature of the experiment')
        self._add_value('float', 'exptl_temperature_uncertainty',
                        modelpath='exptl.temperature_uncertainty',
                        description='temperature of the experiment uncertainty')

    def _init_values_adsnt(self):
        """Initialize adsnt subset of values"""

        self._add_value('str', 'adsnt_degas_summary',
                        modelpath='adsnt.degas_summary',
                        description='summary of degas conditions')
        self._add_value('float', 'adsnt_degas_temperature',
                        modelpath='adsnt.degas_temperature', 
                        description='degas temperature')
        self._add_value('float', 'adsnt_degas_temperature_uncertainty',
                        modelpath='adsnt.degas_temperature_uncertainty', 
                        description='degas temperature uncertainty')
        self._add_value('float', 'adsnt_degas_time',
                        modelpath='adsnt.degas_time', 
                        description='degas time')
        self._add_value('float', 'adsnt_degas_time_uncertainty',
                        modelpath='adsnt.degas_time_uncertainty', 
                        description='degas time uncertainty')
        self._add_value('str', 'adsnt_hashkey',
                        modelpath='adsnt.hashkey', 
                        description='secondary identifier')
        self._add_value('str', 'adsnt_info',
                        modelpath='adsnt.info', 
                        description='secondary identifier')
        self._add_value('str', 'adsnt_material_id',
                        modelpath='adsnt.material_id', 
                        description='designated name for the material')
        self._add_value('float', 'adsnt_sample_density',
                        modelpath='adsnt.sample_density', 
                        description='density of the sample')
        self._add_value('float', 'adsnt_sample_density_uncertainty',
                        modelpath='adsnt.sample_density_uncertainty', 
                        description='density of the sample uncertainty')
        self._add_value('str', 'adsnt_sample_id',
                        modelpath='adsnt.sample_id', 
                        description='unique identifying code used by the operator')
        self._add_value('float', 'adsnt_sample_mass',
                        modelpath='adsnt.sample_mass', 
                        description='mass of the sample')
        self._add_value('float', 'adsnt_sample_mass_uncertainty',
                        modelpath='adsnt.sample_mass_uncertainty', 
                        description='mass of the sample uncertainty')

    def _init_values_simltn(self):
        """Initialize simltn subset of values"""
        self._add_value('str', 'simltn_code',
                        modelpath='simltn.code',
                        description='secondary identifier')
        self._add_value('str', 'simltn_date',
                        modelpath='simltn.date',
                        description='date of the simulation (string in ISO 8601 format)')
        self._add_value('str', 'simltn_forcefield_adsorbent',
                        modelpath='simltn.forcefield_adsorbent',
                        description='adsorbent model details')
        self._add_value('str', 'simltn_forcefield_adsorptive',
                        modelpath='simltn.forcefield_adsorptive',
                        description='adsorptive model details')
        self._add_value('str', 'simltn_input_files',
                        modelpath='simltn.input_files',
                        description='repository link to input files and other codes used in the simulation')
        self._add_value('str', 'simltn_lot',
                        modelpath='simltn.lot',
                        description='level of theory used in calculation, e.g. DFT, MLP, classical etc.')
        self._add_value('str', 'simltn_sampling',
                        modelpath='simltn.sampling',
                        description='phase space sampling algorithm')
        self._add_value('str', 'simltn_size',
                        modelpath='simltn.size',
                        description='num of unit cells, sample mass, etc')
        self._add_value('str', 'simltn_adsorbent_filename',
                        modelpath='simltn.adsorbent_filename',
                        description='filename for adsorbent information')
        self._add_value('str', 'simltn_forcefield_adsnt',
                        modelpath='simltn.forcefield_adsnt',
                        description='adsnt model details')

    def _init_values_units(self):
        """Initialize units subset of values"""
        self._add_value('str', 'units_composition_type',
                        modelpath='units.composition_type',
                        description='composition definiton')
        self._add_value('str', 'units_density',
                        modelpath='units.density',
                        description='units of density')
        self._add_value('str', 'units_loading',
                        modelpath='units.loading',
                        description='units of amount adsorbed')
        self._add_value('str', 'units_mass',
                        modelpath='units.mass',
                        description='units of mass')
        self._add_value('str', 'units_pressure',
                        modelpath='units.pressure',
                        description='units of pressure')
        self._add_value('str', 'units_temperature',
                        modelpath='units.temperature',
                        description='units of temperature')
        self._add_value('str', 'units_time',
                        modelpath='units.time',
                        description='units of time')
        self._add_value('str', 'units_fugacity',
                        modelpath='units.fugacity',
                        description='units of fugacity')
        self._add_value('str', 'units_qst',
                        modelpath='units.qst',
                        description='units of qst')

    def _init_values_citation(self):
        """Initialize citation subset of values"""
        self._add_value('str', 'citation_doi',
                        modelpath='citation.doi',
                        description='the digital object identifier (DOI) of the cited work')
        self._add_value('str', 'citation_source',
                        modelpath='citation.source',
                        description='source of the cited work')

    def _init_values_desorp(self):
        """Initialize desorp subset of values"""
        self._add_value('floatarray', 'desorp_amount',
                        modelpath='desorp.amount',
                        description='amount adsorbed during the desorption measurement')
        self._add_value('floatarray', 'desorp_amount_uncertainty',
                        modelpath='desorp.amount_uncertainty',
                        description='amount adsorbed during the desorption measurement uncertainty')
        self._add_value('floatarray', 'desorp_amount_absolute',
                        modelpath='desorp.amount_absolute',
                        description='absolute amount adsorbed during the desorption measurement')
        self._add_value('floatarray', 'desorp_amount_absolute_uncertainty',
                        modelpath='desorp.amount_absolute_uncertainty',
                        description='absolute amount adsorbed during the desorption measurement uncertainty')
        self._add_value('floatarray', 'desorp_amount_excess',
                        modelpath='desorp.amount_excess',
                        description='excess amount adsorbed during the desorption measurement')
        self._add_value('floatarray', 'desorp_amount_excess_uncertainty',
                        modelpath='desorp.amount_excess_uncertainty',
                        description='excess amount adsorbed during the desorption measurement uncertainty')
        self._add_value('floatarray', 'desorp_amount_net',
                        modelpath='desorp.amount_net',
                        description='net amount adsorbed during the desorption measurement')
        self._add_value('floatarray', 'desorp_amount_net_uncertainty',
                        modelpath='desorp.amount_net_uncertainty',
                        description='net amount adsorbed during the desorption measurement uncertainty')
        self._add_value('floatarray', 'desorp_fugacity',
                        modelpath='desorp.fugacity',
                        description='fugacity of the desorption measurement')
        self._add_value('floatarray', 'desorp_fugacity_uncertainty',
                        modelpath='desorp.fugacity_uncertainty',
                        description='fugacity of the desorption measurement uncertainty')
        self._add_value('floatarray', 'desorp_p0',
                        modelpath='desorp.p0',
                        description='saturation pressure of the desorption measurement at the temperature of the experiment')
        self._add_value('floatarray', 'desorp_p0_uncertainty',
                        modelpath='desorp.p0_uncertainty',
                        description='saturation pressure of the desorption measurement at the temperature of the experiment uncertainty')
        self._add_value('floatarray', 'desorp_pressure',
                        modelpath='desorp.pressure',
                        description='equilibrium pressure of the desorption measurement at the temperature of the experiment')
        self._add_value('floatarray', 'desorp_pressure_uncertainty',
                        modelpath='desorp.pressure_uncertainty',
                        description='equilibrium pressure of the desorption measurement at the temperature of the experiment uncertainty')
    
    def _init_values_adsorp(self):
        """Initialize adsorp subset of values"""
        self._add_value('floatarray', 'adsorp_amount',
                        modelpath='adsorp.amount',
                        description='amount adsorbed during the adsorption measurement')
        self._add_value('floatarray', 'adsorp_amount_uncertainty',
                        modelpath='adsorp.amount_uncertainty',
                        description='amount adsorbed during the adsorption measurement uncertainty')
        self._add_value('floatarray', 'adsorp_amount_absolute',
                        modelpath='adsorp.amount_absolute',
                        description='absolute amount adsorbed during the adsorption measurement')
        self._add_value('floatarray', 'adsorp_amount_absolute_uncertainty',
                        modelpath='adsorp.amount_absolute_uncertainty',
                        description='absolute amount adsorbed during the adsorption measurement uncertainty')
        self._add_value('floatarray', 'adsorp_amount_excess',
                        modelpath='adsorp.amount_excess',
                        description='excess amount adsorbed during the adsorption measurement')
        self._add_value('floatarray', 'adsorp_amount_excess_uncertainty',
                        modelpath='adsorp.amount_excess_uncertainty',
                        description='excess amount adsorbed during the adsorption measurement uncertainty')
        self._add_value('floatarray', 'adsorp_amount_net',
                        modelpath='adsorp.amount_net',
                        description='net amount adsorbed during the adsorption measurement')
        self._add_value('floatarray', 'adsorp_amount_net_uncertainty',
                        modelpath='adsorp.amount_net_uncertainty',
                        description='net amount adsorbed during the adsorption measurement uncertainty')
        self._add_value('floatarray', 'adsorp_enthalpy',
                        modelpath='adsorp.enthalpy',
                        description='enthalpy of adsorption at infinite dilution and low loading')
        self._add_value('floatarray', 'adsorp_enthalpy_uncertainty',
                        modelpath='adsorp.enthalpy_uncertainty',
                        description='enthalpy of adsorption at infinite dilution and low loading uncertainty')
        self._add_value('floatarray', 'adsorp_fugacity',
                        modelpath='adsorp.fugacity',
                        description='fugacity of the adsorption measurement')
        self._add_value('floatarray', 'adsorp_fugacity_uncertainty',
                        modelpath='adsorp.fugacity_uncertainty',
                        description='fugacity of the adsorption measurement uncertainty')
        self._add_value('floatarray', 'adsorp_henry',
                        modelpath='adsorp.henry',
                        description='Henry coefficient describing the infinite-dilution and low-pressure adsorption affinity')
        self._add_value('floatarray', 'adsorp_henry_uncertainty',
                        modelpath='adsorp.henry_uncertainty',
                        description='Henry coefficient describing the infinite-dilution and low-pressure adsorption affinity uncertainty')
        self._add_value('floatarray', 'adsorp_molefraction',
                        modelpath='adsorp.molefraction',
                        description='mole fraction of the adsorptive in the gas phase for a multicomponent adsorption measurement')
        self._add_value('floatarray', 'adsorp_molefraction_uncertainty',
                        modelpath='adsorp.molefraction_uncertainty',
                        description='mole fraction of the adsorptive in the gas phase for a multicomponent adsorption measurement uncertainty')
        self._add_value('floatarray', 'adsorp_p0',
                        modelpath='adsorp.p0',
                        description='saturation pressure of the adsorption measurement at the temperature of the experiment')
        self._add_value('floatarray', 'adsorp_p0_uncertainty',
                        modelpath='adsorp.p0_uncertainty',
                        description='saturation pressure of the adsorption measurement at the temperature of the experiment uncertainty')
        self._add_value('floatarray', 'adsorp_pressure',
                        modelpath='adsorp.pressure',
                        description='equilibrium pressure of the adsorption measurement')
        self._add_value('floatarray', 'adsorp_pressure_uncertainty',
                        modelpath='adsorp.pressure_uncertainty',
                        description='equilibrium pressure of the adsorption measurement uncertainty')
        self._add_value('floatarray', 'adsorp_selectivity',
                        modelpath='adsorp.selectivity',
                        description='adsorption selectivity for a specified component pair under the given conditions')
        self._add_value('floatarray', 'adsorp_selectivity_uncertainty',
                        modelpath='adsorp.selectivity_uncertainty',
                        description='adsorption selectivity for a specified component pair under the given conditions uncertainty')
        self._add_value('floatarray', 'adsorp_qst',
                        modelpath='adsorp.qst',
                        description='adsorption qst')
        self._add_value('floatarray', 'adsorp_qst_uncertainty',
                        modelpath='adsorp.qst_uncertainty',
                        description='adsorption qst uncertainty')

    def read_aif(self, aif, explicit_key_check=True):

        # Read in file contents using gemmi.cif parser
        with uber_open_rmode(aif) as f:
            doc = cif.read_string(f.read())

        assert len(doc) == 1, 'AIF files with multiple blocks not supported!'
        block = doc[0]
        self.name = block.name

        for item in block:

            # Extract single value "pair" entries
            if item.pair is not None:
                key, value = item.pair
                if explicit_key_check and key[1:] not in self.valuenames:
                    raise ValueError(f'Unrecognized AIF term {key}')
                setattr(self, key[1:], value.strip("'"))

            # Extract looped values
            elif item.loop is not None:
                keys = item.loop.tags
                values = np.array(item.loop.values, dtype=float).reshape(-1, len(keys))
                for i, key in enumerate(keys):
                    if explicit_key_check and key[1:] not in self.valuenames:
                        raise ValueError(f'Unrecognized AIF term {key}')
                    setattr(self, key[1:], values[:,i])
        
    def build_aif(self, output_file=None, loop_fmt='%.5E'):
        doc = cif.Document()
        block = doc.add_new_block(self.name)

        desorp_keys = []
        adsorp_keys = []
        for name, obj in zip(self.valuenames, self.value_objects):
            if obj.value is None:
                continue
        
            cat = name.split('_')[0]
            if cat == 'desorp':
                desorp_keys.append(name[7:])
            elif cat == 'adsorp':
                adsorp_keys.append(name[7:])
            else:
                block.set_pair(f'_{name}', cif.quote(str(obj.value)))

        if len(desorp_keys) > 0:
            desorp_loop = block.init_loop('_desorp_', desorp_keys)
            
            desorp_values = []
            for key in desorp_keys:
                desorp_values.append([loop_fmt % val for val in getattr(self, f'desorp_{key}')])
            desorp_loop.set_all_values(desorp_values) 

        if len(adsorp_keys) > 0:
            adsorp_loop = block.init_loop('_adsorp_', adsorp_keys)
            
            adsorp_values = []
            for key in adsorp_keys:
                adsorp_values.append([loop_fmt % val for val in getattr(self, f'adsorp_{key}')])
            adsorp_loop.set_all_values(adsorp_values) 

        if output_file is None:
            return block.as_string()
        else:
            doc.write_file(output_file)
                    