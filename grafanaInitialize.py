import os
import argparse
from grafanaInterface import GrafanaManager, GrafanaInitalizer

# Constants

DEFAULT_CONFIG_FILE_NAME = 'config.txt'
DEFAULT_CONFIG_FILE_DELIMITER = '-'
DEFAULT_DASHBOARD_DIRECTORY = 'Dashboards'

# Local Methods

def parseArguments():
    ap = argparse.ArgumentParser()

    ap.add_argument("--host", help="Grafana Host")
    ap.add_argument("--user", help="Grafana Username Login")
    ap.add_argument("--password", help="Grafana User Password")

    return ap.parse_args()

def createConfigFile(fileName=DEFAULT_CONFIG_FILE_NAME, delimiter=DEFAULT_CONFIG_FILE_DELIMITER, host=None, key=None):
    if host is None:
        print("ERROR: No host found")
        print("WARNING: No config file created")
        return 
    
    if key is None:
        print("ERROR: No key found")
        print("WARNING: No config file created")
        return

    with open(fileName, 'w') as cf:
        cf.write('host' + delimiter + host + '\n')
        cf.write('apiKey' + delimiter + key)


def initializeGrafana(interface, dashboardDir):
    # Upload dashboards inside dashboard Dir
    for root, dirs, files in os.walk(DEFAULT_DASHBOARD_DIRECTORY):
        for file in files:
            interface.createDashboard(dashboardDir + '/' + file)

def main():
    args = parseArguments()

    if args.host is None:
        print("ERROR: No host specified")
        return 
    if args.user is None:
        print("ERROR: Username not specified")
        return
    if args.password is None:
        print("ERROR: Password not specified")
        return

    initializer = GrafanaInitalizer(args.host, args.user, args.password)

    host = initializer.getHost()
    key = initializer.getkey()

    createConfigFile(DEFAULT_CONFIG_FILE_NAME, DEFAULT_CONFIG_FILE_DELIMITER, host, key)

    interface = GrafanaManager(host, key)

    initializeGrafana(interface, DEFAULT_DASHBOARD_DIRECTORY)

if __name__ == "__main__":
    main()
    