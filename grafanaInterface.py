import requests

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