import requests, json, os
from os.path import exists
from urllib3.exceptions import InsecureRequestWarning

# Settings

# Prevents invalid certificate warning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning) 

def createConfigFile(fileName, delimiter, host, key):
    """
    Creates configuration file containing host and generated API Token

    :param fileName: The path and file for where to create configuration file
    :type fileName: str
    :param delimiter: The delimiter of the configuration file
    :type delimiter: str
    :param host: Grafana Host
    :type host: str
    :param key: Grafana generated API Token
    :type key: str
    """

    with open(fileName, 'w') as cf:
        cf.write('host' + delimiter + host + '\n')
        cf.write('apiKey' + delimiter + key)

def parseConfigFile(configFile, delimiter):
    """
    Reads config file containing host and generated API Token

    :param configFile: The configuration file path
    :type configFile: str
    :param delimiter: The delimiter of the configuration file
    :type delimiter: str
    :raises: Exception: if config file not found
    :return: host containing Grafana Host
    :rtype: str 
    :return: generated API Token
    :rtype: str
    """
    host = None
    key = None

    # Check if the configuration file exists
    if(exists(configFile)):
        # Assign default host and key 
        with open(configFile, 'r') as cf:
            for currentLine in cf:
                line = currentLine.split(delimiter)
                if(line[0] == 'host'):
                    host = str(line[1]).strip()
                elif(line[0] == 'apiKey'):
                    key = str(line[1]).strip()
    else:
        raise Exception("Configuration file not found")
    
    return host, key

class GrafanaManager(object):
    """
    Grafana Manager interacts with Grafana Host using Grafana's REST APIs 

    :param host: Grafana Host 
    :type host: str
    :param username: Grafana Admin Username
    :type username: str
    :param password: Grafana Admin Password
    :type password: str
    :param key: Grafana API token
    :type key: str
    """
    def __init__(self, host=None, username=None, password=None, key=None):
        """
        Constructor Method
        """
        self.host = host 
        self.apiKey = key

        self.username = username
        self.password = password
    
    def getHost(self):
        return self.host
    
    def setHost(self, host):
        self.host = host
    
    def getAPIKey(self):
        return self.apiKey

    def setAPIKey(self, key):
        self.apiKey = key
    
    def getUsername(self):
        return self.username
    
    def setUsername(self, username):
        self.username = username
    
    def getPassword(self):
        return self.password

    def setPassword(self, password):
        self.password = password
    
    def setUserLogin(self, username, password):
        self.username = username
        self.password = password
    
    def createNewUser(self, newUserName, newUserEmail, newUserLogin, newUserPassword):
        """
        Creates new Grafana user, automatically assigning to default organization

        :param newUserName: New Grafana User Name
        :type newUserName: str
        :param newUserEmail: New Grafana User Email
        :type newUserEmail: str
        :param newUserLogin: New Grafana User Login Username
        :type newUserLogin: str
        :param newUserPassword: New Grafana User Password
        :type newUserPassword: str
        :raises: Exception: if object has no username or password
        :raises: Exception: if no host given to object
        :return: response of API call
        :rtype: response
        """

        session = requests.session()

        newUser = {
            "name": newUserName, 
            "email": newUserEmail, 
            "login": newUserLogin, 
            "password": newUserPassword
        }

        if self.password is None or self.username is None:
            # Raise exception for object lacking username or password
            raise Exception("No password or username specified")
        
        if self.host is not None:
            # Login to Grafana
            session.post(
                'https://' + self.host + '/grafana/login', 
                headers={'Content-Type': 'application/json'},
                json={"password": self.password,"user": self.username}, 
                verify=False
            )
            # Create New User
            x = session.post(
                'https://' + self.host + '/grafana/api/admin/users', 
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, 
                json=newUser, 
                verify=False
            )

            return x
        else:
            # Raise exception for key error when there is no host for API token creation
            raise Exception("No host specified")
    
    def findUser(self, credential):
        session = requests.session()

        if self.password is None or self.username is None:
            # Raise exception for object lacking username or password
            raise Exception("No password or username specified")
        
        if self.host is not None:
            # Login to Grafana
            session.post(
                'https://' + self.host + '/grafana/login', 
                headers={'Content-Type': 'application/json'},
                json={"password": self.password,"user": self.username}, 
                verify=False
            )
            # Find User
            x = session.get(
                'https://' + self.host + '/grafana/api/users/lookup?loginOrEmail=' + str(credential), 
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, 
                verify=False
            )

            return x
        else:
            # Raise exception for key error when there is no host for API token creation
            raise Exception("No host specified")
    
    def changePassword(self, credential, newPassword):
        session = requests.session()

        if self.password is None or self.username is None:
            # Raise exception for object lacking username or password
            raise Exception("No password or username specified")
        
        if self.host is not None:
            # Login to Grafana
            session.post(
                'https://' + self.host + '/grafana/login', 
                headers={'Content-Type': 'application/json'},
                json={"password": self.password,"user": self.username}, 
                verify=False
            )

            # Find user with credential
            response = self.findUser(credential)
            # Return none if user does not exist
            if response.status_code != 200:
                return None

            # Get User ID
            userId = json.loads(response.text)['id']

            # Change Password
            x = session.put(
                'https://' + self.host + '/grafana/api/admin/users/' + str(userId) + '/password', 
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, 
                json={"password": newPassword},
                verify=False
            )

            return x
        else:
            # Raise exception for key error when there is no host for API token creation
            raise Exception("No host specified")

    def changeAdminPermission(self, credential, makeAdmin):
        session = requests.session()

        if self.password is None or self.username is None:
            # Raise exception for object lacking username or password
            raise Exception("No password or username specified")
        
        if self.host is not None:
            # Login to Grafana
            session.post(
                'https://' + self.host + '/grafana/login', 
                headers={'Content-Type': 'application/json'},
                json={"password": self.password,"user": self.username}, 
                verify=False
            )

            # Find user with credential
            response = self.findUser(credential)
            # Return none if user does not exist
            if response.status_code != 200:
                return None

            # Get User ID
            userId = json.loads(response.text)['id']

            # Change Password
            x = session.put(
                'https://' + self.host + '/grafana/api/admin/users/' + str(userId) + '/permissions', 
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, 
                json={"isGrafanaAdmin": makeAdmin},
                verify=False
            )

            return x
        else:
            # Raise exception for key error when there is no host for API token creation
            raise Exception("No host specified")

    def createAdminToken(self, tokenName="newToken"):
        """
        Generate new admin API token for object

        :param tokenName: New Token Name 
        :type tokenName: str
        :raises: Exception: if object has no username or password
        :raises: Exception: if API token already created
        :raises: Exception: if no host given to object
        """

        session = requests.session()

        if self.password is None or self.username is None:
            # Raise exception for object lacking username or password
            raise Exception("No password or username specified")

        if self.host is not None:
            try:
                # Login to Grafana
                session.post(
                    'https://' + self.host + '/grafana/login', 
                    headers={'Content-Type': 'application/json'},
                    json={"password": self.password,"user": self.username}, 
                    verify=False
                )
                # Get API key
                x = session.post(
                    'https://' + self.host + '/grafana/api/auth/keys', 
                    headers={'Content-Type': 'application/json'}, 
                    json={"name": tokenName, "role":"Admin"}, 
                    verify=False
                )

                self.apiKey = json.loads(x.text)['key']
            except KeyError:
                # Raise exception for key error when there is an existing API token
                self.apiKey = None
                raise Exception("API token already exists")
        else:
            # Raise exception for key error when there is no host for API token creation
            raise Exception("No host specified")
 
    def createDashboard(self, fileDir):
        """
        Uploads given dashboard to Grafana host 

        :param fileDir: Path to JSON containing Grafana dashboard
        :type fileDir: str
        :raises: Exception: if object has no existing host file
        :raises: Exception: if object has no existing API key
        :return: response of API call
        :rtype: response
        """
        if self.host is None:
            raise Exception("No host specified")

        if self.apiKey is None:
            raise Exception("No admin API key specified")

        url = 'https://' + self.host + '/grafana/api/dashboards/db'

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
            'Authorization': "Bearer " + self.apiKey
        }

        dashboardObject = open(fileDir).read()

        x = requests.post(url, headers=headers, data=dashboardObject, verify=False)
        return x

    def deleteDashboard(self, dashboardUID):
        """
        Deletes given dashboard unique ID in Grafana host 

        :param dashboardUID: Grafana Dashboard Unique ID, usually written within JSON
        :type dashboardUID: str
        :raises: Exception: if object has no existing host file
        :raises: Exception: if object has no existing API key
        :return: response of API call
        :rtype: response
        """
        if self.host is None:
            raise Exception("No host specified")

        if self.apiKey is None:
            raise Exception("No admin API key specified")

        url = 'https://' + self.host + '/grafana/api/dashboards/uid/' + dashboardUID

        headers = {
            'Authorization': "Bearer " + self.apiKey
        }

        x = requests.delete(url, headers=headers, verify=False)
        return x

    def findDashboard(self, dashboardUID):
        """
        Locates given dashboard unique ID in Grafana host 

        :param dashboardUID: Grafana Dashboard Unique ID, usually written within JSON
        :type dashboardUID: str
        :raises: Exception: if object has no existing host file
        :raises: Exception: if object has no existing API key
        :return: response of API call
        :rtype: response
        """
        if self.host is None:
            raise Exception("No host specified")

        if self.apiKey is None:
            raise Exception("No admin API key specified")

        url = 'https://' + self.host + '/grafana/api/dashboards/uid/' + dashboardUID

        headers = {
            'Authorization': "Bearer " + self.apiKey
        }

        x = requests.get(url, headers=headers, verify=False)
        return x
    
    def getHomeDashboard(self):
        """
        Locates home dashboard in Grafana host

        :param dashboardUID: Grafana Dashboard Unique ID, usually written within JSON
        :type dashboardUID: str
        :raises: Exception: if object has no existing host file
        :raises: Exception: if object has no existing API key
        :return: response of API call
        :rtype: response
        """
        if self.host is None:
            raise Exception("No host specified")

        if self.apiKey is None:
            raise Exception("No admin API key specified")

        url = 'https://' + self.host + '/grafana/api/dashboards/home'

        headers = {
            'Authorization': "Bearer " + self.apiKey
        }

        x = requests.get(url, headers=headers, verify=False)
        return x
    
    def uploadDashboards(self, dashboardDir):
        """
        Uploads each dashboard in given directory containing 
        valid host and Grafana API key

        :param dashboardDir: Path containing directory of dashboards to be uplaoded
        :type dashboardDir: str
        :return: dictionary of dashboard file names and their upload status 
        :rtype: dictionary (key = str, value = response)
        """
        dashboardUploadStatus = {}
        for root, dirs, files in os.walk(dashboardDir):
            for file in files:
                response = self.createDashboard(dashboardDir + '/' + file)
                dashboardUploadStatus[file] = response
        return dashboardUploadStatus