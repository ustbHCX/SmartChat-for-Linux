import time

from Cache import CacheUtils
from Interface import Page
from MessageRecord import RecordUtils
from Net import TCP
from Utils import Log

message_path = r"Data\HistoryMessage"


class Status:
    success = b'0000'
    login_error_pwd = b'0001'
    not_reg = b'0010'
    have_reg = b'0011'
    error_pwd = b'0100'
    have_informed = b'0101'
    not_admin = b'0110'
    member_banned = b'0111'
    online = b'1000'
    undefined = b'1111'


class Prefix:
    user_register = b'0000'
    user_login = b'0001'
    user_logout = b'0010'
    user_set_pwd = b'0011'

    user_friend_operate = b'0110'
    admin_group_operate = b'0111'

    contacts_info = b'1000'
    contact_delete = b'1001'

    notices = b'1100'

    message = b'1111'


class Notice:
    friend_application = '1'
    group_application = '2'


def sendMessage(message):
    # 1.获取当前用户
    user = CacheUtils.getCurrentUser()
    if user is None:
        Log.console("您还没有登录！")
        return

    # 2.获取发送目标
    current_contact_id = user.getCurrentContactId()
    if current_contact_id is None:
        Log.console("您还没有选择发送对象！")
        return

    # 3.发送消息
    user_id = user.getId()
    addr = CacheUtils.getServerAddr()
    buff = Prefix.message + bytes(user_id + " " + current_contact_id + " " + message, "utf8")
    post_back = TCP.connect(addr, buff)

    # 4.查询是否被禁言
    if post_back == Prefix.message + Status.member_banned:
        Log.console("您已被禁言！")
        return

    # 5.显示消息
    RecordUtils.addMessage(message, user_id, current_contact_id, "0")
    Page.messageBoxUpdate(RecordUtils.getMessages(user_id, current_contact_id))
    Page.show()


def analyze(buff):
    prefix = getPrefix(buff)
    params = getParams(buff)

    # 解析当前用户数据
    user_data = CacheUtils.getCurrentUser()

    # 检查当前是否有用户登录
    while user_data is None:
        user_data = CacheUtils.getCurrentUser()
        time.sleep(0.1)

    user_id = user_data.getId()

    # 接受到当前用户的联系人信息
    if prefix == Prefix.contacts_info:
        user_data.setContacts(params)
        Page.contactsBoxUpdate(user_data.getContacts())
        Page.show()

    # 接受到联系人发来的消息
    elif prefix == Prefix.message:
        message = params[0][-1]
        for i in range(1, len(params)):
            message = message + " " + params[i][0]
        # 解析目标ID
        contact_id = params[0][0]

        # 解析是否为群消息，写入聊天记录
        if len(params[0]) == 3:
            # 解析消息
            RecordUtils.addMessage(message, user_id, contact_id, params[0][1])
        else:
            # 解析消息
            RecordUtils.addMessage(message, user_id, contact_id, "1")

        # 如果该消息是从正在聊天的用户发来的，则直接显示
        if contact_id == user_data.getCurrentContactId():
            Page.messageBoxUpdate(RecordUtils.getMessages(user_id, contact_id))
            Page.show()
        else:
            user_data.addContactUnreadNum(contact_id)
            Page.contactsBoxUpdate(user_data.getContacts())
            Page.show()

    # 接受到通知消息
    elif prefix == Prefix.notices:
        for i in params:
            # 解析联系人
            contact_id = i[0]

            # 好友通知
            if len(i) == 2:
                # 解析通知类型
                notice = i[1]

                # 好友申请
                if notice == Notice.friend_application:
                    user_data.addFriendApplication(contact_id)
                    if user_data.getCurrentContactId() is None:
                        Page.messageBoxUpdate(user_data.getApplicationMessages())
                        Page.show()

            # 群通知
            elif len(i) == 3:
                # 解析群成员
                member_id = i[1]

                # 解析通知类型
                notice = i[2]

                # 入群申请
                if notice == Notice.group_application:
                    user_data.addGroupApplication(contact_id, member_id)
                    if user_data.getCurrentContactId() is None:
                        Page.messageBoxUpdate(user_data.getApplicationMessages())
                        Page.show()

    # 接受到删除好友/群踢出消息
    elif prefix == Prefix.contact_delete:
        for i in params:
            if i[0] in user_data.getContactsId():
                user_data.delContact(i[0])
                Page.contactsBoxUpdate(user_data.getContacts())
                Page.show()
                Log.console("您失去了与" + i[0] + "的联系")


def getPrefix(buff: bytes):
    return buff[0:4]


def getParams(buff: bytes):
    datas = str(buff[4:], "utf8").split(" ")
    params = []
    for i in datas:
        params.append(i.split(":"))
    return params
