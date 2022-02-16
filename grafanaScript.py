import argparse
from os.path import exists

from grafanaInterface import GrafanaManager

# Constants

CONFIG_FILE_NAME = 'config.txt'
CONFIG_FILE_DELIMITER = '-'

# Local methods
def parseConfigFile(configFile, delimiter):
    host = None
    key = None

    # Assign default host and key if configuration file exists
    if(exists(configFile)):
        with open(configFile, 'r') as cf:
            for currentLine in cf:
                line = currentLine.split(delimiter)
                if(line[0] == 'host'):
                    host = str(line[1]).strip()
                elif(line[0] == 'apiKey'):
                    key = str(line[1]).strip()
    
    return host, key

def parseArguments():
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
    MANUAL_HOST, MANUAL_KEY = parseConfigFile(CONFIG_FILE_NAME, CONFIG_FILE_DELIMITER)

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
            interface.createDashboard(args.file)
        elif(args.mode == 'find'):
            interface.findDashboard(args.uniqueID)
        elif(args.mode == 'delete'):
            interface.deleteDashboard(args.uniqueID)
        elif(args.mode == 'home'):
            interface.getHomeDashboard()
        else:
            print("No matching call for " + args.mode)

if __name__ == "__main__":
    main()