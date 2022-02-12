import os
from grafanaInterface import GrafanaManager

# CONSTANTS

DEFAULT_CONFIG_FILE_NAME = 'config.txt'
DEFAULT_CONFIG_FILE_DELIMITER = '-'
DEFAULT_DASHBOARD_DIRECTORY = 'Dashboards'

def getHost():
    pass

def getKey():
    pass

def createConfigFile(fileName=DEFAULT_CONFIG_FILE_DELIMITER, host=None, key=None):
    if host is None:
        print("ERROR: No host found")
        return None
    
    if key is None:
        print("ERROR: No key found")
        return None

    with open(fileName, 'w') as cf:
        cf.write('host' + DEFAULT_CONFIG_FILE_DELIMITER + host + '\n')
        cf.write('key' + DEFAULT_CONFIG_FILE_DELIMITER + key)


def initializeGrafana(interface, dashboardDir):
    # Upload dashboards inside dashboard Dir
    for root, dirs, files in os.walk(DEFAULT_DASHBOARD_DIRECTORY):
        for file in files:
            interface.createDashboard(dashboardDir + '/' + file)

def main():
    host = getHost()
    key = getKey()

    file = createConfigFile(DEFAULT_CONFIG_FILE_NAME, host, key)

    if file is None:
        print("WARNING: No config file created")

    interface = GrafanaManager(host, key)

    initializeGrafana(interface, DEFAULT_DASHBOARD_DIRECTORY)

if __name__ == "__main__":
    main()
    