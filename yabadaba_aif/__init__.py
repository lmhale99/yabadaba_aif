from yabadaba import databasemanager, recordmanager

# Add the modular Record styles
recordmanager.import_style('aif', '.AIF', __name__)
recordmanager.import_style('aif2', '.AIF2', __name__)

# Add the modular Database styles
databasemanager.import_style('aif', '.AIFDatabase', __name__)