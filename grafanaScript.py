import argparse
from os.path import exists

from grafanaInterface import GrafanaManager, parseConfigFile

# Constants

DEFAULT_CONFIG_FILE_NAME = 'config.txt'
DEFAULT_CONFIG_FILE_DELIMITER = '-'

# Local methods

def parseArguments():
    """ Parses command arguments """  
    ap = argparse.ArgumentParser()

    ap.add_argument("--host", help="Set Grafana Host")
    ap.add_argument("--key", help="Set Grafana admin API key")
    ap.add_argument("-m", "--mode", help="API call to make: create, update, find, delete, home")
    ap.add_argument("-uid", "--uniqueID", help="Unique ID of dashboard")
    ap.add_argument("-f", "--file", help="File name of dashboard JSON")

    return ap.parse_args()

def main():
    args = parseArguments()

    # Manual Configuration of host and key
    MANUAL_HOST, MANUAL_KEY = parseConfigFile(DEFAULT_CONFIG_FILE_NAME, DEFAULT_CONFIG_FILE_DELIMITER)

    interface = GrafanaManager(MANUAL_HOST, MANUAL_KEY)

    # Override manual configuration if specified in arguments
    if args.host is not None:
        interface.setHost(args.host)
    if args.key is not None:
        interface.setAPIKey(args.key)

    # Direct to correspending REST API call if mode is specified
    if args.mode is not None:
        args.mode = args.mode.lower()
        if(args.mode == 'create' or args.mode == 'update'):
            res = interface.createDashboard(args.file)
            print(res)
        elif(args.mode == 'find'):
            res = interface.findDashboard(args.uniqueID)
            print(res)
        elif(args.mode == 'delete'):
            res = interface.deleteDashboard(args.uniqueID)
            print(res)
        elif(args.mode == 'home'):
            res = interface.getHomeDashboard()
            print(res)
        else:
            print("No matching call for " + args.mode)

if __name__ == "__main__":
    main()