import socket
import time

from Cache import Groups
from Net import NetUtils
from Log import LogUtils


def main():
    # 配置服务器信息
    # host = "127.0.0.1"
    host='10.23.253.43'
    port = 10000

    # 开启服务器
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    LogUtils.log("服务器已开启，本机地址: " + str((host, port)))

    # 初始化群聊
    Groups.initGroups()

    # 主循环
    while 1:
        # 监听
        sock, addr = s.accept()
        buff = sock.recv(1024)
        LogUtils.log("TCP got connection form " + str(sock.getpeername()) + '    ' +
                     "Message: " + str(buff, "utf8"))
        if not buff:
            break
        else:
            # 解析报文
            prefix = NetUtils.getPrefix(buff)
            params = NetUtils.getParams(buff)

            # 回传
            NetUtils.analyze(prefix, params, sock)
            sock.close()
        time.sleep(0.3)


main()
