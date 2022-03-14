import os
import argparse
from os.path import exists
from grafanaInterface import GrafanaManager, GrafanaInitalizer, createConfigFile, parseConfigFile

# Constants

DEFAULT_CONFIG_FILE_NAME = 'config.txt'
DEFAULT_CONFIG_FILE_DELIMITER = '-'
DEFAULT_DASHBOARD_DIRECTORY = 'Dashboards'

# Local Methods

def parseArguments():
    """ Parses command arguments """   
    ap = argparse.ArgumentParser()

    ap.add_argument("--host", help="Grafana Host")
    ap.add_argument("--user", help="Grafana Username Login")
    ap.add_argument("--password", help="Grafana User Password")

    return ap.parse_args()

def uploadDashboards(interface, dashboardDir):
    """
    Uploads each dashboard in given directory through given interface

    Args:
        interface (str): Grafana Interface Object 
        dashboardDir (str): Directory containing dashboards to be uploaded
    Returns:
        None
    """
    for root, dirs, files in os.walk(DEFAULT_DASHBOARD_DIRECTORY):
        for file in files:
            response = interface.createDashboard(dashboardDir + '/' + file)
            if response.status_code == 200:
                print(f"{file} was successfully uploaded")
            else:
                print(f"{file} was unsuccessfully uploaded")

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

    if exists(DEFAULT_CONFIG_FILE_NAME):
        host, key = parseConfigFile(DEFAULT_CONFIG_FILE_NAME, DEFAULT_CONFIG_FILE_DELIMITER)
    else:
        initializer = GrafanaInitalizer(args.host, args.user, args.password)

        host = initializer.getHost()
        key = initializer.getkey()

        # Creates config file containing host and generated API Token
        createConfigFile(DEFAULT_CONFIG_FILE_NAME, DEFAULT_CONFIG_FILE_DELIMITER, host, key)

    interface = GrafanaManager(host, key)

    # Uploads each dashboard within dashboard directory to host Grafana
    uploadDashboards(interface, DEFAULT_DASHBOARD_DIRECTORY)

if __name__ == "__main__":
    main()
    