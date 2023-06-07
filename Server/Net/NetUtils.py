from Cache import Groups, OnlineUsers
from Group import GroupUtils
from Log import LogUtils
from Net import TCP
from TemporaryMessage import MessageUtils
from User import UserUtils


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



class Operates:
    add = '1'
    delete = '2'
    confirm = '3'
    refuse = '4'
    ban = '5'
    unban = '6'
    kick = '7'


def getPrefix(buff: bytes):
    return buff[0:4]


def getParams(buff: bytes):
    return str(buff[4:], "utf8").split(" ")


def analyze(prefix, params, socket):
    # 用户注册
    if prefix == Prefix.user_register:
        status = UserUtils.regUser(params[0], params[1])
        LogUtils.log("用户" + params[0] + "请求注册", status)
        socket.send(prefix + status)

    # 账户登录
    elif prefix == Prefix.user_login:
        user_id = params[0]
        user_pwd = params[1]
        user_ip = params[2]
        user_port = params[3]
        ret, status = UserUtils.login(user_id, user_pwd)
        LogUtils.log("用户" + params[0] + "请求登录", status)
        socket.send(prefix + status)
        # 登录成功
        if ret:
            # 将该用户信息加入在线列表
            user_data = UserUtils.UserData(user_id)
            addr = (user_ip, int(user_port))
            OnlineUsers.setOnlineUserAddr(user_id, addr)

            # 发送该用户好友在线信息
            online_friends_id, offline_friends_id, groups_id = user_data.getContacts()
            message = ''
            for i in online_friends_id:
                message = message + i + ":" + UserUtils.Friend.online_friend + " "
            for i in offline_friends_id:
                message = message + i + ":" + UserUtils.Friend.offline_friend + " "
            for i in groups_id:
                message = message + i + ":" + UserUtils.Friend.group + " "
            TCP.connect(addr, Prefix.contacts_info + bytes(message.rstrip(), "utf8"))

            # 发送群信息 todo

            # 发送好友通知消息
            applications = user_data.getApplications()
            if applications:
                message = ''
                for i in applications:
                    message = message + i + ":" + UserUtils.Notice.application + " "
                TCP.connect(addr, Prefix.notices + bytes(message.rstrip(), "utf8"))

            # 更新群信息
            groups_id = Groups.getGroupsId()
            for i in groups_id:
                group_data = Groups.getGroupData(i)
                # 检查是否为管理员
                if user_id in group_data.getAdmins():
                    # 管理员上线
                    group_data.addOnlineAdmin(user_id)
                    for j in group_data.getApplications():
                        buff = Prefix.notices + bytes(i + ":" + j + ":" + GroupUtils.Notice.application, "utf8")
                        TCP.connect(addr, buff)

            # 发送暂存消息
            for i in MessageUtils.getOfflineMessagesById(user_id):
                TCP.connect(addr, bytes(i.rstrip(), 'utf8'))
            MessageUtils.clearOfflineMessageById(user_id)

            # 向所有好友广播该用户已登录
            for i in online_friends_id:
                addr = OnlineUsers.getOnlineUserAddr(i)
                buff = Prefix.contacts_info + bytes(user_id + ":" + UserUtils.Friend.online_friend, "utf8")
                TCP.connect(addr, buff)

    # 用户退出
    elif prefix == Prefix.user_logout:

        user_id = params[0]
        if OnlineUsers.isOnline(user_id):
            user_data = UserUtils.UserData(user_id)
            online_friends_id, ret, ret = user_data.getContacts()

            # 向所有好友广播该用户已退出
            for i in online_friends_id:
                addr = OnlineUsers.getOnlineUserAddr(i)
                buff = Prefix.contacts_info + bytes(user_id + ":" + UserUtils.Friend.offline_friend, "utf8")
                TCP.connect(addr, buff)
            OnlineUsers.delOnlineUser(user_id)

            # 管理员下线
            groups = Groups.getGroupsId()
            for i in groups:
                group_data = Groups.getGroupData(i)
                admins = group_data.getAdmins()
                if user_id in admins:
                    group_data.delOnlineAdmin(user_id)
            socket.send(prefix + LogUtils.Status.success)
            LogUtils.log("用户" + params[0] + "用户退出")

    # 用户改密
    elif prefix == Prefix.user_set_pwd:
        user_id = params[0]
        old_pwd = params[1]
        new_pwd = params[2]
        if old_pwd == UserUtils.getPwd(user_id):
            UserUtils.setPwd(user_id, new_pwd)
            socket.send(prefix + LogUtils.Status.success)
        else:
            socket.send(prefix + LogUtils.Status.error_pwd)

    # 消息转发
    elif prefix == Prefix.message:
        # 发送方账号
        src = params[0]
        # 目标账号
        dst = params[1]
        # 群消息
        if dst in Groups.getGroupsId():
            # 获得群数据
            group_data = Groups.getGroupData(dst)

            # 查询是否在群中
            if src not in group_data.getMembers():
                socket.send(prefix + LogUtils.Status.undefined)
                return

            # 查询是否被禁言
            banned_members = group_data.getBannedMembers()
            if src in banned_members:
                socket.send(prefix + LogUtils.Status.member_banned)
                return

            # 转发给所有群用户

            message = " ".join(params[2:]).rstrip()

            # 获取群成员
            members = group_data.getMembers()
            online_users_id = OnlineUsers.getOnlineUsers()
            for i in members:
                # 排除自己
                if i == src:
                    continue

                # 查询是否在线
                elif i in online_users_id:
                    addr = OnlineUsers.getOnlineUserAddr(i)
                    # 编辑发送信息
                    buff = Prefix.message + bytes(dst + ':' + src + ':' + message, "utf8")
                    # 将信息转发给目标用户
                    TCP.connect(addr, buff)

                # 未在线暂存消息
                else:
                    # 编辑发送信息
                    buff = Prefix.message + bytes(dst + ':' + src + ':' + message, "utf8")
                    # 暂存消息
                    MessageUtils.addOfflineMessageById(i, buff)
            socket.send(prefix + LogUtils.Status.success)

        # 用户消息
        else:
            # 查询是否为好友
            if src not in UserUtils.UserData(dst).getFriends():
                socket.send(prefix + LogUtils.Status.undefined)
                return

            # 解析消息
            message = " ".join(params[2:]).rstrip()

            # 查询是否在线
            if dst in OnlineUsers.getOnlineUsers():
                # 获取目标地址
                addr = OnlineUsers.getOnlineUserAddr(dst)
                # 将信息转发给目标用户
                TCP.connect(addr, Prefix.message + bytes(src + ':' + message, "utf8"))

            # 未在线暂存消息
            else:
                # 暂存消息
                buff = Prefix.message + bytes(src + ':' + message, "utf8")
                MessageUtils.addOfflineMessageById(dst, buff)
            socket.send(prefix + LogUtils.Status.success)

    # 用户操作
    elif prefix == Prefix.user_friend_operate:
        src = params[0]
        dst = params[1]
        operate = params[2]
        LogUtils.log(src + "对用户" + dst + "进行操作" + operate)
        # 添加好友
        if operate == Operates.add:
            # 判断对方是否存在
            if not UserUtils.isReg(dst):
                # 判断对方是否为群
                if dst in Groups.getGroupsId():
                    group_data = Groups.getGroupData(dst)
                    group_data.addApplication(src)
                    online_admins = group_data.getOnlineAdmins()
                    for i in online_admins:
                        addr = OnlineUsers.getOnlineUserAddr(i)
                        buff = Prefix.notices + bytes(dst + ":" + src + ":" + GroupUtils.Notice.application, "utf8")
                        TCP.connect(addr, buff)
                    LogUtils.log(src + "申请加入群" + dst)
                    socket.send(prefix + LogUtils.Status.success)
                else:
                    socket.send(prefix + LogUtils.Status.not_reg)
            else:
                # 添加通知
                UserUtils.UserData(dst).addApplication(src)
                # 对方在线则转发通知
                if dst in OnlineUsers.getOnlineUsers():
                    addr = OnlineUsers.getOnlineUserAddr(dst)
                    buff = Prefix.notices + bytes(src + ":" + UserUtils.Notice.application, "utf8")
                    TCP.connect(addr, buff)
                LogUtils.log(src + "请求添加" + dst + "为好友")
                socket.send(prefix + LogUtils.Status.success)

        # 删除好友
        elif operate == Operates.delete:
            # 删除好友信息
            UserUtils.UserData(dst).delFriend(src)
            UserUtils.UserData(src).delFriend(dst)
            if OnlineUsers.isOnline(dst):
                addr = OnlineUsers.getOnlineUserAddr(dst)
                TCP.connect(addr, Prefix.contact_delete + bytes(src, 'utf8'))
            socket.send(prefix + LogUtils.Status.success)

        # 同意添加好友
        elif operate == Operates.confirm:
            if dst in UserUtils.UserData(src).getApplications():
                src_data = UserUtils.UserData(src)
                dst_data = UserUtils.UserData(dst)
                src_data.addFriend(dst)
                dst_data.addFriend(src)
                # 删除通知
                src_data.delApplication(dst)
                if dst in OnlineUsers.getOnlineUsers():
                    addr = OnlineUsers.getOnlineUserAddr(src)
                    buff = Prefix.contacts_info + bytes(dst + ":" + UserUtils.Friend.online_friend, "utf8")
                    TCP.connect(addr, buff)

                    addr = OnlineUsers.getOnlineUserAddr(dst)
                    buff = Prefix.contacts_info + bytes(src + ":" + UserUtils.Friend.online_friend, "utf8")
                    TCP.connect(addr, buff)
                else:
                    addr = OnlineUsers.getOnlineUserAddr(src)
                    buff = Prefix.contacts_info + bytes(dst + ":" + UserUtils.Friend.offline_friend, "utf8")
                    TCP.connect(addr, buff)
                socket.send(prefix + LogUtils.Status.success)

        # 拒绝添加好友
        elif operate == Operates.refuse:
            # 删除好友通知
            UserUtils.UserData(src).delApplication(dst)
            socket.send(prefix + LogUtils.Status.success)

    # 管理员操作
    elif prefix == Prefix.admin_group_operate:
        # 解析参数
        src = params[0]
        group_id = params[1]
        dst = params[2]
        operate = params[3]

        # 查询该群是否存在
        if group_id not in Groups.getGroupsId():
            socket.send(prefix + LogUtils.Status.not_reg)
            return

        # 查询该用户是否为管理员
        group_data = Groups.getGroupData(group_id)
        admins = group_data.getAdmins()
        if src not in admins:
            socket.send(prefix + LogUtils.Status.not_admin)
            return

        LogUtils.log("群" + group_id + "管理员" + src + "对成员" + dst + "进行操作" + operate)

        # 同意进群
        if operate == Operates.confirm:
            # 将目标用户加入到群成员中
            group_data.addMember(dst)

            # 将群加入目标用户联系人中
            UserUtils.UserData(dst).addGroup(group_id)

            # 删除该入群申请
            group_data.delApplication(dst)

            # 在线则发送群信息
            if OnlineUsers.isOnline(dst):
                addr = OnlineUsers.getOnlineUserAddr(dst)
                buff = Prefix.contacts_info + bytes(group_id + ":" + UserUtils.Friend.group, "utf8")
                TCP.connect(addr, buff)

        # 拒绝进群
        elif operate == Operates.refuse:
            # 删除该入群申请
            group_data.delApplication(dst)

        # 用户禁言
        elif operate == Operates.ban:
            group_data.banMember(dst)

        # 用户解禁
        elif operate == Operates.unban:
            group_data.unbanMember(dst)

        # 踢出用户
        elif operate == Operates.kick:
            # 从用户联系人列表里删除该群
            group_data.delMember(dst)

            # 群成员中删除该用户
            UserUtils.UserData(dst).delGroup(group_id)

            # 在线则发出被踢出通知
            if OnlineUsers.isOnline(dst):
                addr = OnlineUsers.getOnlineUserAddr(dst)
                TCP.connect(addr, Prefix.contact_delete + bytes(group_id, 'utf8'))

        socket.send(prefix + LogUtils.Status.success)

    else:
        socket.send(prefix + LogUtils.Status.undefined)
