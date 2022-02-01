import requests
import argparse
from os.path import exists

from urllib3.exceptions import InsecureRequestWarning

# Constants

CONFIG_FILE_NAME = 'config.txt'

# Settings

# Prevents invalid certificate warning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning) 

class GrafanaManager(object):
    def __init__(self, host=None, key=None):
        self.host = host 
        self.apiKey = key
    
    def getHost(self):
        return self.host
    
    def setHost(self, host):
        self.host = host
    
    def getAPIKey(self):
        return self.apiKey

    def setAPIKey(self, key):
        self.apiKey = key
 
    # POST Methods

    def createDashboard(self, fileDir):
        if self.host is None:
            print("ERROR: No host specified")
            return 

        if self.apiKey is None:
            print("ERROR: No admin API key specified")
            return

        url = 'https://' + self.host + '/grafana/api/dashboards/db'

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
            'Authorization': "Bearer " + self.apiKey
        }

        dashboardObject = open(fileDir).read()

        x = requests.post(url, headers=headers, data=dashboardObject, verify=False)
        print(x)
    
    # DELETE Methods

    def deleteDashboard(self, dashboardUID):
        if self.host is None:
            print("ERROR: No host specified")
            return 

        if self.apiKey is None:
            print("ERROR: No admin API key specified")
            return

        url = 'https://' + self.host + '/grafana/api/dashboards/uid/' + dashboardUID

        headers = {
            'Authorization': "Bearer " + self.apiKey
        }

        x = requests.delete(url, headers=headers, verify=False)
        print(x)

    # GET Methods

    def findDashboard(self, dashboardUID):
        if self.host is None:
            print("ERROR: No host specified")
            return 

        if self.apiKey is None:
            print("ERROR: No admin API key specified")
            return

        url = 'https://' + self.host + '/grafana/api/dashboards/uid/' + dashboardUID

        headers = {
            'Authorization': "Bearer " + self.apiKey
        }

        x = requests.get(url, headers=headers, verify=False)
        print(x)
    
    def getHomeDashboard(self):
        if self.host is None:
            print("ERROR: No host specified")
            return 

        if self.apiKey is None:
            print("ERROR: No admin API key specified")
            return

        url = 'https://' + self.host + '/grafana/api/dashboards/home'

        headers = {
            'Authorization': "Bearer " + self.apiKey
        }

        x = requests.get(url, headers=headers, verify=False)
        print(x)

# Local methods
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
    # Arguments will override manual configuration
    MANUAL_HOST = None
    MANUAL_KEY = None

    # Assign default host and key if configuration file exists
    if(exists(CONFIG_FILE_NAME)):
        with open(CONFIG_FILE_NAME, 'r') as cf:
            pass

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