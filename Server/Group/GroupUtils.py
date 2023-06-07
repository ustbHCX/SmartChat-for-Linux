import os

import ReadData

group_data_path = r"Group/Data"


class Notice:
    application = "2"


class GroupData:
    def __init__(self, group_id):
        self.group_id = group_id
        self.__path = os.path.abspath(os.path.join(group_data_path, group_id + ".txt"))
        self.__data = ReadData.getData(self.__path)
        self.__online_admins = []
        self.__online_members = []

    def getOnlineAdmins(self):
        return self.__online_admins

    def addOnlineAdmin(self, admin):
        self.__online_admins.append(admin)

    def delOnlineAdmin(self, admin):
        self.__online_admins.remove(admin)

    def getAdmins(self):
        return self.__data['admin']

    def getMembers(self):
        return self.__data['member']

    def addMember(self, dst):
        if dst not in self.__data['member']:
            self.__data['member'].append(dst)
            ReadData.setData(self.__path, self.__data)

    def delMember(self, dst):
        if dst in self.__data['member']:
            self.__data['member'].remove(dst)
            ReadData.setData(self.__path, self.__data)

    def getApplications(self):
        return self.__data['application']

    def addApplication(self, application):
        if application not in self.__data['application']:
            self.__data['application'].append(application)
            ReadData.setData(self.__path, self.__data)

    def delApplication(self, application):
        if application in self.__data['application']:
            self.__data['application'].remove(application)
            ReadData.setData(self.__path, self.__data)

    def getBannedMembers(self):
        return self.__data['banned']

    def banMember(self, dst):
        if dst not in self.__data['banned']:
            self.__data['banned'].append(dst)
            ReadData.setData(self.__path, self.__data)

    def unbanMember(self, dst):
        if dst in self.__data['banned']:
            self.__data['banned'].remove(dst)
            ReadData.setData(self.__path, self.__data)
