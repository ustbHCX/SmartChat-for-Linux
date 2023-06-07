import socket
import time

from Cache import CacheUtils
from Net import NetUtils
from Utils import Properties

properties_path = "data.properties"


def connect(dest_addr, send_data: bytes):
    #  1.建立套接字socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #  2.建立连接
    try:
        tcp_socket.connect(dest_addr)
    except OSError:
        try:
            tcp_socket.connect(("127.0.0.1", 10000))
        except OSError:
            print("连接服务器失败")

    #  3.发送数据
    tcp_socket.send(send_data)
    #  4.接收数据
    buff = tcp_socket.recv(1024)

    #  5.关闭套接字
    tcp_socket.close()

    #  6.返回数据
    return buff


def listen():
    #  建立套接字socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET表示使用ipv4,SOCK_DGRAM表示使用UDP通信协议
    properties = Properties.Properties(properties_path).getProperties()

    #  绑定端口port
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_host = s.getsockname()[0]
    local_port = int(properties['local_port'])
    local_addr = (local_host, local_port)
    s.close()

    while True:
        try:
            tcp_socket.bind(local_addr)  # 绑定端口
        except OSError:
            local_port = local_port + 1
            local_addr = (local_host, local_port)
        else:
            break

    #  保存地址信息
    CacheUtils.setLocalAddr(local_addr)
    CacheUtils.setServerAddr((properties['serv_host'], int(properties['serv_port'])))

    #  开启监听
    tcp_socket.listen(2)
    while True:
        sock, addr = tcp_socket.accept()
        #  接收数据
        buff = sock.recv(1024)  # 定义单次最大接收字节数
        #  回传数据
        sock.send(buff[0:4])
        #  解析数据
        NetUtils.analyze(buff)
        # print("TCP got connection form " + str(sock.getpeername()) + '    ' + "Message: " + str(buff, "utf8"))
        if not buff:
            break

        # 延时
        time.sleep(0.1)

    #  关闭套接字
    tcp_socket.close()
