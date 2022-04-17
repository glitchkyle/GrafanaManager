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
    :return: Function Status
    :rtype: JSON dictionary
    """
    response = {
        "success": False,
        "msg": None
    }

    with open(fileName, 'w') as cf:
        cf.write('host' + delimiter + host + '\n')
        cf.write('apiKey' + delimiter + key)
        response['success'] = True
        response['msg'] = "Successfully created configuration file."
    
    return response

def parseConfigFile(configFile, delimiter):
    """
    Reads config file containing host and generated API Token

    :param configFile: The configuration file path
    :type configFile: str
    :param delimiter: The delimiter of the configuration file
    :type delimiter: str
    :return: Function Status
    :rtype: JSON dictionary
    """
    response = {
        "success": False,
        "msg": None
    }

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
                    response['host'] = host
                elif(line[0] == 'apiKey'):
                    key = str(line[1]).strip()
                    response['key'] = key
            response['success'] = True
            response['msg'] = "Successfully parsed config file."
    else:
        response['msg'] = "No config file found. Failed to parse config file."

    return response

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
        :return: Function Status
        :rtype: JSON dictionary 
        """
        response = {
        "success": False,
        "msg": None
        }

        session = requests.session()

        newUser = {
            "name": newUserName, 
            "email": newUserEmail, 
            "login": newUserLogin, 
            "password": newUserPassword
        }

        if self.password is None:
            response['msg'] = "No Grafana host admin password specified to object."
            return response
        
        if self.username is None:
            response['msg'] = "No Grafana host username specified to object."
            return response
        
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

            if x.status_code == 200:
                response['success'] = True
                response['msg'] = "Successfully created new Grafana user."
                response['data'] = x
            else:
                response['msg'] = "Failed to create new Grafana user."
                response['data'] = x
        else:
            response['msg'] = "No Grafana host specified to object."

        return response
    
    def findUser(self, credential):
        """
        Find Grafana user

        :param credential: Grafana username or email to find
        :type credential: str
        :return: Function Status
        :rtype: JSON dictionary 
        """
        response = {
        "success": False,
        "msg": None
        }

        session = requests.session()

        if self.password is None:
            response['msg'] = "No Grafana host admin password specified to object."
            return response
        
        if self.username is None:
            response['msg'] = "No Grafana host username specified to object."
            return response
        
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

            if x.status_code == 200:
                response['success'] = True
                response['msg'] = "Successfully found Grafana user."
                response['data'] = x
            else:
                response['msg'] = "Failed to find Grafana user."
                response['data'] = x
        else:
            response['msg'] = "No Grafana host specified to object."

        return response
    
    def changePassword(self, credential, newPassword):
        """
        Change Grafana user password

        :param credential: Grafana username or email to be updated
        :type credential: str
        :param newPassword: New Password of given user
        :type newPassword: str
        :return: Function Status
        :rtype: JSON dictionary 
        """
        response = {
        "success": False,
        "msg": None
        }

        session = requests.session()

        if self.password is None:
            response['msg'] = "No Grafana host admin password specified to object."
            return response
        
        if self.username is None:
            response['msg'] = "No Grafana host username specified to object."
            return response
        
        if self.host is not None:
            # Login to Grafana
            session.post(
                'https://' + self.host + '/grafana/login', 
                headers={'Content-Type': 'application/json'},
                json={"password": self.password,"user": self.username}, 
                verify=False
            )

            # Find user with credential
            jsonResponse = self.findUser(credential)

            responseData = jsonResponse['data']

            # Return if user does not exist
            if responseData.status_code != 200:
                response['msg'] = "Failed to change password. User not found."
                response['data'] = responseData
                return response

            # Get User ID
            userId = json.loads(responseData.text)['id']

            # Change Password
            x = session.put(
                'https://' + self.host + '/grafana/api/admin/users/' + str(userId) + '/password', 
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, 
                json={"password": newPassword},
                verify=False
            )

            if x.status_code == 200:
                response['success'] = True
                response['msg'] = "Successfully changed password for Grafana user."
                response['data'] = x
            else:
                response['msg'] = "Failed to change password for Grafana user."
                response['data'] = x
        else:
            response['msg'] = "No Grafana host specified to object."

        return response

    def changeAdminPermission(self, credential, makeAdmin):
        """
        Change Grafana user admin permissions

        :param credential: Grafana username or email to be updated
        :type credential: str
        :param makeAdmin: Give Admission Permission
        :type makeAdmin: bool
        :return: Function Status
        :rtype: JSON dictionary 
        """
        response = {
        "success": False,
        "msg": None
        }

        session = requests.session()

        if self.password is None:
            response['msg'] = "No Grafana host admin password specified to object."
            return response
        
        if self.username is None:
            response['msg'] = "No Grafana host username specified to object."
            return response
        
        if self.host is not None:
            # Login to Grafana
            session.post(
                'https://' + self.host + '/grafana/login', 
                headers={'Content-Type': 'application/json'},
                json={"password": self.password,"user": self.username}, 
                verify=False
            )

            # Find user with credential
            jsonResponse = self.findUser(credential)

            responseData = jsonResponse['data']

            # Return if user does not exist
            if responseData.status_code != 200:
                response['msg'] = "Failed to change admin permissions. User not found."
                response['data'] = responseData
                return response

            # Get User ID
            userId = json.loads(responseData.text)['id']

            # Change Admin Permission
            x = session.put(
                'https://' + self.host + '/grafana/api/admin/users/' + str(userId) + '/permissions', 
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, 
                json={"isGrafanaAdmin": makeAdmin},
                verify=False
            )

            if x.status_code == 200:
                response['success'] = True
                response['msg'] = "Successfully changed admin permissions for Grafana user."
                response['data'] = x
            else:
                response['msg'] = "Failed to change admin permissions for Grafana user."
                response['data'] = x
        else:
            response['msg'] = "No Grafana host specified to object."

        return response

    def createAdminToken(self, tokenName="newToken"):
        """
        Generate new admin API token for object

        :param tokenName: Name of new token
        :type tokenName: str
        :return: Function Status
        :rtype: JSON dictionary 
        """
        response = {
        "success": False,
        "msg": None
        }

        session = requests.session()

        if self.password is None:
            response['msg'] = "No Grafana host admin password specified to object."
            return response
        
        if self.username is None:
            response['msg'] = "No Grafana host username specified to object."
            return response

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

                if x.status_code == 200:
                    self.apiKey = json.loads(x.text)['key']
                    response['success'] = True
                    response['msg'] = "Successfully created new Grafana API token."
                    response['data'] = x
                else:
                    response['msg'] = "Failed to create new Grafana API token."
                    response['data'] = x
            except KeyError:
                response['msg'] = "Grafana API token with given name has already been created."
        else:
            response['msg'] = "No Grafana host specified to object."

        return response
 
    def createDashboard(self, fileDir):
        """
        Generate new admin API token for object

        :param fileDir: Path to JSON containing Grafana dashboard
        :type fileDir: str
        :return: Function Status
        :rtype: JSON dictionary 
        """
        response = {
        "success": False,
        "msg": None
        }

        if self.password is None:
            response['msg'] = "No Grafana host admin password specified to object."
            return response
        
        if self.username is None:
            response['msg'] = "No Grafana host username specified to object."
            return response

        url = 'https://' + self.host + '/grafana/api/dashboards/db'

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
            'Authorization': "Bearer " + self.apiKey
        }

        dashboardObject = open(fileDir).read()

        x = requests.post(url, headers=headers, data=dashboardObject, verify=False)

        if x.status_code == 200:
            response['success'] = True
            response['msg'] = "Successfully uploaded dashboard."
            response['data'] = x
        else:
            response['msg'] = "Failed to upload dashboard."
            response['data'] = x
        
        return response

    def deleteDashboard(self, dashboardUID):
        """
        Deletes given dashboard unique ID in Grafana host 

        :param dashboardUID: Grafana Dashboard Unique ID, usually written within JSON
        :type dashboardUID: str
        :return: Function Status
        :rtype: JSON dictionary 
        """
        response = {
        "success": False,
        "msg": None
        }

        if self.password is None:
            response['msg'] = "No Grafana host admin password specified to object."
            return response
        
        if self.username is None:
            response['msg'] = "No Grafana host username specified to object."
            return response

        url = 'https://' + self.host + '/grafana/api/dashboards/uid/' + dashboardUID

        headers = {
            'Authorization': "Bearer " + self.apiKey
        }

        x = requests.delete(url, headers=headers, verify=False)

        if x.status_code == 200:
            response['success'] = True
            response['msg'] = "Successfully deleted dashboard."
            response['data'] = x
        else:
            response['msg'] = "Failed to delete dashboard."
            response['data'] = x
        
        return response


    def findDashboard(self, dashboardUID):
        """
        Locates given dashboard unique ID in Grafana host 

        :param dashboardUID: Grafana Dashboard Unique ID, usually written within JSON
        :type dashboardUID: str
        :return: Function Status
        :rtype: JSON dictionary 
        """
        response = {
        "success": False,
        "msg": None
        }

        if self.password is None:
            response['msg'] = "No Grafana host admin password specified to object."
            return response
        
        if self.username is None:
            response['msg'] = "No Grafana host username specified to object."
            return response

        url = 'https://' + self.host + '/grafana/api/dashboards/uid/' + dashboardUID

        headers = {
            'Authorization': "Bearer " + self.apiKey
        }

        x = requests.get(url, headers=headers, verify=False)
        
        if x.status_code == 200:
            response['success'] = True
            response['msg'] = "Successfully found dashboard."
            response['data'] = x
        else:
            response['msg'] = "Failed to find dashboard."
            response['data'] = x
        
        return response
    
    def getHomeDashboard(self):
        """
        Locates home dashboard in Grafana host

        :param dashboardUID: Grafana Dashboard Unique ID, usually written within JSON
        :type dashboardUID: str
        :return: Function Status
        :rtype: JSON dictionary 
        """
        response = {
        "success": False,
        "msg": None
        }

        if self.password is None:
            response['msg'] = "No Grafana host admin password specified to object."
            return response
        
        if self.username is None:
            response['msg'] = "No Grafana host username specified to object."
            return response

        url = 'https://' + self.host + '/grafana/api/dashboards/home'

        headers = {
            'Authorization': "Bearer " + self.apiKey
        }

        x = requests.get(url, headers=headers, verify=False)
        
        if x.status_code == 200:
            response['success'] = True
            response['msg'] = "Successfully found home dashboard."
            response['data'] = x
        else:
            response['msg'] = "Failed to find home dashboard."
            response['data'] = x
        
        return response
    
    def uploadDashboards(self, dashboardDir):
        """
        Uploads all dashboards in given dashboard directory

        :param dashboardDir: Path containing directory of dashboards to be uploaded
        :type dashboardDir: str
        :return: Function Status
        :rtype: JSON dictionary 
        """
        response = {
        "success": False,
        "msg": None
        }
        dashboardUploadStatus = {}
        for root, dirs, files in os.walk(dashboardDir):
            for file in files:
                response = self.createDashboard(dashboardDir + '/' + file)
                dashboardUploadStatus[file] = response
        response['success'] = True
        response['msg'] = "Successfully uploaded dashboards"
        response['data'] = dashboardUploadStatus
        return response