from grafanaInterface import *
import unittest, requests

# Prevents invalid certificate warning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning) 

host = str(input())
username = str(input())
password = str(input())
token = str(input())

interface = GrafanaManager(host, username, password, token)

class TestGrafanaMethods(unittest.TestCase):
    def test_CreateConfigFile(self):
        result = createConfigFile('configFile.txt', '-', host, token)
        self.assertEqual(True, result['success'], result['msg'])
    
    def test_ParseConfigFile(self):
        result = parseConfigFile('configFile.txt', '-')
        self.assertEqual(True, result['success'], result['msg'])

    def test_CreateNewUser(self):
        result = interface.createNewUser('user', 'user@user.com', 'userLogin', 'uesrPassword')
        self.assertEqual(True, result['success'], result['msg'])

    def test_FindUser(self):
        result = interface.findUser('userLogin')
        self.assertEqual(True, result['success'], result['msg'])

    # def test_ChangePassword(self):
    #     result = interface.changePassword('userLogin', 'newPassword')
    #     self.assertEqual(True, result['success'], result['msg'])

    # def test_ChangeAdminPermission(self):
    #     result = interface.changeAdminPermission('userLogin', True)
    #     self.assertEqual(True, result['success'], result['msg'])

    def test_CreateAdminToken(self):
        result = interface.createAdminToken()
        self.assertEqual(True, result['success'], result['msg'])

    def test_CreateDashboard(self):
        result = interface.createDashboard('Dashboards/networkDashboard.json')
        self.assertEqual(True, result['success'], result['msg'])
    
    # def test_FindDashboard(self):
    #     result = interface.findDashboard('dHEquNzGz')
    #     self.assertEqual(True, result['success'], result['msg'])

    def test_DeleteDashboard(self):
        result = interface.deleteDashboard('dHEquNzGz')
        self.assertEqual(True, result['success'], result['msg'])

    def test_GetHomeDashboard(self):
        result = interface.getHomeDashboard()
        self.assertEqual(True, result['success'], result['msg'])

    def test_UploadDashboards(self):
        result = interface.uploadDashboards('Dashboards')
        self.assertEqual(True, result['success'], result['msg'])

if __name__ == "__main__":
    unittest.main()