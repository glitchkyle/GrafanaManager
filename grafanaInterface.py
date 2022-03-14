import requests
import json
from urllib3.exceptions import InsecureRequestWarning

# Settings

# Prevents invalid certificate warning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning) 

def createConfigFile(fileName, delimiter, host, key):
    """
    Creates config file containing host and generated API Token

    Args:
        fileName (str): File name for config file (default DEFAULT_CONFIG_FILE_NAME)
        delimiter (str): Delimiter for config file (default DEFAULT_CONFIG_FILE_DELIMITER)
        host (str): Grafana Host 
        key (str): Grafana newly generated API Token 
    Returns: 
        None 
    """
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

def parseConfigFile(configFile, delimiter):
    """
    Reads config file containing host and generated API Token

    Args:
        fileName (str): File name for config file (default DEFAULT_CONFIG_FILE_NAME)
        delimiter (str): Delimiter for config file (default DEFAULT_CONFIG_FILE_DELIMITER)
    Returns:
        host, key (str, str): Values stored in config file
    """
    host = None
    key = None

    # Assign default host and key if configuration file exists
    with open(configFile, 'r') as cf:
        for currentLine in cf:
            line = currentLine.split(delimiter)
            if(line[0] == 'host'):
                host = str(line[1]).strip()
            elif(line[0] == 'apiKey'):
                key = str(line[1]).strip()
    
    return host, key

class GrafanaInitalizer(object):
    """
    Grafana Initializer stores the given host and attempts to create a 
    a new Grafana API token

    Attributes:
        host (str): Grafana Host
        key (str): Grafana API token to be generated
    """
    def __init__(self, host, username, password):
        """
        Grafana Initializer Constructor

        Args: 
            host (str): Grafana Host 
            username (str): Grafana Admin Username
            password (str): Grafana Admin Password 
        Returns:
            None
        """
        self.host = None
        self.key = None

        # Get Host
        self.host = host

        # Get Key
        if self.host is not None:
            session = requests.session()
            
            try:
                # Login to Grafana
                session.post(
                    'https://' + self.host + '/grafana/login', 
                    headers={'Content-Type': 'application/json'},
                    json={"password": password,"user":username}, 
                    verify=False
                )
                # Get API key
                x = session.post(
                    'https://' + self.host + '/grafana/api/auth/keys', 
                    headers={'Content-Type': 'application/json'}, 
                    json={"name":"newAPI", "role":"Admin"}, 
                    verify=False
                )

                self.key = json.loads(x.text)['key']
            except KeyError:
                print("ERROR: API token already exists")
                self.key = None

    def getHost(self):
        return self.host

    def setHost(self, host):
        self.host = host

    def getkey(self):
        return self.key

    def setkey(self, key):
        self.key = key

class GrafanaManager(object):
    """
    Grafana Manager interacts with Grafana using Grafana's REST APIs 

    Attributes:
        host (str): Grafana Host
        apikey (str): Generated Grafana admin API key 
    """
    def __init__(self, host=None, key=None):
        """
        Grafana Initializer Constructor

        Args: 
            host (str): Grafana Host (default None)
            key (str): Grafana admin API key (default None)
        Returns:
            None
        """
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
        """
        Uploads given dashboard to Grafana host 

        Args: 
            fileDir (str): Dashboard JSON file directory
        Returns:
            None
        """
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
        return x
    
    # DELETE Methods

    def deleteDashboard(self, dashboardUID):
        """
        Deletes given dashboard unique ID in Grafana host 

        Args: 
            dashboardUID (str): Dashboard Unique ID 
        Returns:
            None
        """
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
        return x

    # GET Methods

    def findDashboard(self, dashboardUID):
        """
        Locates given dashboard unique ID in Grafana host 

        Args: 
            dashboardUID (str): Dashboard Unique ID 
        Returns:
            None
        """
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
        return x
    
    def getHomeDashboard(self):
        """
        Locates home dashboard in Grafana host

        Args: 
            None
        Returns:
            None
        """
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
        return x