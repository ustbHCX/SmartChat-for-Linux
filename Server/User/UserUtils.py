import os

import ReadData
from Cache import OnlineUsers
from Log import LogUtils


user_data_path = r"User/Data"
message_path = r"TemporaryMessage/Data"



def isReg(user_id: str):
    path = os.path.join(user_data_path, user_id + ".txt")
    path = os.path.abspath(path)
    return os.access(path, os.F_OK)


def setPwd(user_id: str, pwd):
    path = user_data_path + "/" + user_id + ".txt"
    path = os.path.abspath(path)
    data = ReadData.getData(path)
    data['password'][0] = pwd
    ReadData.setData(user_id, data)


def getPwd(user_id: str):
    path = user_data_path + "/" + user_id + ".txt"
    path = os.path.abspath(path)
    return ReadData.getData(path)['password'][0]


def regUser(user: str, pwd: str, nick: str = 'user'):
    path = user_data_path + "/" + user + ".txt"
    path = os.path.abspath(path)

    # 判断账号信息是否存在
    if isReg(user):
        return LogUtils.Status.have_reg

    # 创建账号信息文件
    os.open(os.path.join(message_path, user + ".txt"), os.O_CREAT)
    os.open(path, os.O_CREAT | os.O_RDWR)
    file = open(path, 'a+')

    # 初始化信息
    file.write("id:" + user + "\n")
    file.write("password:" + pwd + "\n")
    file.write("nick:" + nick + "\n")
    file.write("friend:" + "\n")
    file.write("group:" + "\n")
    file.write("application:" + "\n")

    file.close()

    # 返回注册成功
    return LogUtils.Status.success


def login(user_id: str, pwd: str):
    # 判断账号信息是否存在
    if not isReg(user_id):
        return False, LogUtils.Status.not_reg
    # 判断密码是否正确
    elif pwd != getPwd(user_id):
        return False, LogUtils.Status.error_pwd
    # 判断是否在线
    elif OnlineUsers.isOnline(user_id):
        return False, LogUtils.Status.online
    # 返回登录成功
    else:
        return True, LogUtils.Status.success


class Notice:
    application = "1"


class Friend:
    online_friend = "1"
    offline_friend = "0"
    group = "2"


class UserData:
    def __init__(self, user_id):
        self.user_id = user_id
        self.__path = os.path.abspath(os.path.join(user_data_path, user_id + ".txt"))
        self.__data = ReadData.getData(self.__path)
        self.__user_addr = ()

    def getPassword(self):
        return self.__data['password'][0]

    def setPassword(self, pwd: str):
        self.__data['pwd'][0] = pwd
        ReadData.setData(self.__path, self.__data)

    def getFriends(self):
        return self.__data['friend']

    def addFriend(self, dst):
        if dst not in self.__data['friend']:
            self.__data['friend'].append(dst)
            ReadData.setData(self.__path, self.__data)

    def delFriend(self, dst):
        if dst in self.__data['friend']:
            self.__data['friend'].remove(dst)
            ReadData.setData(self.__path, self.__data)

    def getGroups(self):
        return self.__data['group']

    def addGroup(self, dst):
        if dst not in self.__data['group']:
            self.__data['group'].append(dst)
            ReadData.setData(self.__path, self.__data)

    def delGroup(self, dst):
        if dst in self.__data['group']:
            self.__data['group'].remove(dst)
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

    def getContacts(self):
        friends_id = self.getFriends()
        online_users_id = OnlineUsers.getOnlineUsers()
        online_friends_id = []
        offline_friends_id = []
        for i in friends_id:
            if i in online_users_id:
                online_friends_id.append(i)
            else:
                offline_friends_id.append(i)
        groups_id = self.getGroups()
        return online_friends_id, offline_friends_id, groups_id
