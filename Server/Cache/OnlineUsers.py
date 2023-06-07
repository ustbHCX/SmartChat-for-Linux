ol_users_addr = {}


def getOnlineUsers():
    return ol_users_addr.keys()


def getOnlineUserAddr(user_id):
    return ol_users_addr[user_id]


def setOnlineUserAddr(user_id, user_addr):
    ol_users_addr[user_id] = user_addr


def delOnlineUser(user_id):
    if user_id in ol_users_addr.keys():
        del ol_users_addr[user_id]


def isOnline(user_id):
    if user_id in ol_users_addr.keys():
        return True
    else:
        return False
