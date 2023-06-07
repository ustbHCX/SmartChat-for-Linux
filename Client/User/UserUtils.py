import os

from Cache import CacheUtils
from MessageRecord import RecordUtils
from Net import TCP, NetUtils
from Utils import Log

record_path = r"MessageRecord/Data"


# 注册
def register(user_id, pwd):
    # 编写通信信息
    buff = NetUtils.Prefix.user_register + bytes(user_id + " " + pwd, 'utf8')
    try:
        # 解析数据
        post_back = TCP.connect(CacheUtils.getServerAddr(), buff)
        if post_back == NetUtils.Prefix.user_register + NetUtils.Status.success:
            Log.console("注册成功")
        elif post_back == NetUtils.Prefix.user_register + NetUtils.Status.have_reg:
            Log.console("账号已经注册")
    except ConnectionRefusedError:
        Log.console("未找到服务器")


# 登录
def login(user_id, pwd):
    # 获取本地tcp监听地址
    local_host = CacheUtils.getLocalAddr()[0]
    local_port = str(CacheUtils.getLocalAddr()[1])

    # 向服务器发送登录请求
    buff = NetUtils.Prefix.user_login + bytes(user_id + " " + pwd + " " + local_host + " " + local_port, 'utf8')

    try:
        # 解析数据
        post_back = TCP.connect(CacheUtils.getServerAddr(), buff)

        # 返回结果
        if post_back == NetUtils.Prefix.user_login + NetUtils.Status.success:
            # 添加当前用户
            user = User(user_id)
            CacheUtils.setCurrentUser(user)
            # 建立用户聊天记录文件夹
            path = os.path.join(record_path, user_id)
            path = os.path.abspath(path)
            if not os.path.exists(path):
                os.makedirs(path)
            Log.console("登录成功")
        elif post_back == NetUtils.Prefix.user_login + NetUtils.Status.not_reg:
            Log.console("当前账户未注册")
        elif post_back == NetUtils.Prefix.user_login + NetUtils.Status.error_pwd:
            Log.console("密码错误")
        elif post_back == NetUtils.Prefix.user_login + NetUtils.Status.online:
            Log.console("此用户已经在线")
        else:
            Log.console("未知错误，登录失败")
    except ConnectionRefusedError:
        Log.console("未找到服务器")


# 改密码
def setPwd(user_id, old_pwd, new_pwd):
    buff = NetUtils.Prefix.user_set_pwd + bytes(user_id + " " + old_pwd + " " + new_pwd, "utf8")
    post_back = TCP.connect(CacheUtils.getServerAddr(), buff)
    if post_back == NetUtils.Prefix.user_set_pwd + NetUtils.Status.success:
        Log.console("修改成功")
    elif post_back == NetUtils.Prefix.user_set_pwd + NetUtils.Status.error_pwd:
        Log.console("旧密码错误")


class User:
    def __init__(self, user_id):
        self.__user_id = user_id
        self.__contacts = {}
        self.__groups = []
        self.__current_contact = None
        self.__friend_applications = []
        self.__group_applications = {}

    def getId(self):
        return self.__user_id

    # 登出
    def logout(self):
        # 保存未读信息数量
        for i in zip(self.__contacts.keys(), self.__contacts.values()):
            RecordUtils.setUnreadNum(self.__user_id, i[0], [str(i[1][0])])
        buff = NetUtils.Prefix.user_logout + bytes(self.__user_id, "utf8")
        post_back = TCP.connect(CacheUtils.getServerAddr(), buff)
        if post_back == NetUtils.Prefix.user_logout + NetUtils.Status.success:
            Log.console("您已退出此账号")

    # 好友操作
    def friendOperate(self, friend_id, operate_id):
        buff = NetUtils.Prefix.user_friend_operate + bytes(self.__user_id + " " + friend_id + " " + operate_id,
                                                           "utf8")
        post_back = TCP.connect(CacheUtils.getServerAddr(), buff)
        if post_back == NetUtils.Prefix.user_friend_operate + NetUtils.Status.not_reg:
            Log.console("未找到对方账号")
        elif post_back == NetUtils.Prefix.user_friend_operate + NetUtils.Status.success:
            Log.console("操作成功")

    # 群聊操作
    def groupOperate(self, group_id, member_id, operate_id):
        buff = NetUtils.Prefix.admin_group_operate + bytes(
            self.__user_id + " " + group_id + " " + member_id + " " + operate_id, "utf8")
        post_back = TCP.connect(CacheUtils.getServerAddr(), buff)
        if post_back == NetUtils.Prefix.admin_group_operate + NetUtils.Status.not_reg:
            Log.console("未找到对方账号")
        elif post_back == NetUtils.Prefix.user_friend_operate + NetUtils.Status.success:
            Log.console("操作成功")

    # 读写联系人信息
    def getContactsId(self):
        return self.__contacts.keys()

    def getContacts(self):
        return self.__contacts

    def setContacts(self, params):
        if params[0][0] == '':
            return
        for i in params:
            contact_id = i[0]
            unread_num = RecordUtils.getUnreadNum(self.__user_id, contact_id)
            print(unread_num)
            if i[1] == "0":
                self.__contacts[contact_id] = [unread_num, "Friend(Offline)"]
            elif i[1] == "1":
                self.__contacts[contact_id] = [unread_num, "Friend"]
            elif i[1] == "2":
                self.__contacts[contact_id] = [unread_num, "Group"]
                self.__groups.append(contact_id)

    def delContact(self, contact_id):
        if contact_id in self.__contacts.keys():
            self.__contacts.pop(contact_id)

    # 设置联系人未读消息数量
    def addContactUnreadNum(self, contact_id):
        self.__contacts[contact_id][0] = self.__contacts[contact_id][0] + 1

    def clearContactUnreadNum(self, contact_id):
        self.__contacts[contact_id][0] = 0

    # 读写好友申请
    def getFriendApplications(self):
        return self.__friend_applications

    def addFriendApplication(self, friend_id):
        if friend_id not in self.__friend_applications:
            self.__friend_applications.append(friend_id)

    def delFriendApplication(self, friend_id):
        if friend_id in self.__friend_applications:
            self.__friend_applications.remove(friend_id)

    # 读写群聊申请
    def getGroupApplications(self, group_id):
        if group_id in self.__group_applications.keys():
            return self.__group_applications[group_id]
        else:
            return []

    def addGroupApplication(self, group_id, member_id):
        if group_id in self.__group_applications.keys():
            if member_id not in self.__group_applications[group_id]:
                self.__group_applications[group_id].append(member_id)
        else:
            self.__group_applications[group_id] = []
            self.__group_applications[group_id].append(member_id)

    def delGroupApplication(self, group_id, member_id):
        if member_id in self.__group_applications[group_id]:
            self.__group_applications[group_id].remove(member_id)

    # 解析通知信息
    def getApplicationMessages(self):
        application_messages = []
        for i in self.getFriendApplications():
            application_messages.append([i, 16, "请求添加您为好友"])
        for j in self.__groups:
            for i in self.getGroupApplications(j):
                application_messages.append([i, 10 + len(j), "请求加入群" + j])
        return application_messages

    # 读写当前选中联系人
    def getCurrentContactId(self):
        return self.__current_contact

    def setCurrentContactId(self, contact_id):
        self.__current_contact = contact_id
