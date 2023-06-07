__current_user = None
__local_addr = None
__server_addr = None


def getCurrentUser():
    return __current_user


def setCurrentUser(user):
    global __current_user
    __current_user = user


def getLocalAddr():
    return __local_addr


def setLocalAddr(addr):
    global __local_addr
    __local_addr = addr


def getServerAddr():
    return __server_addr


def setServerAddr(addr):
    global __server_addr
    __server_addr = addr
