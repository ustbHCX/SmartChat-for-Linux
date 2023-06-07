import socket

from Log import LogUtils


def connect(dest_addr, send_data: bytes):
    try:
        #  1.建立套接字socket
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #  2.建立连接
        tcp_socket.connect(dest_addr)

        #  3.收发数据
        tcp_socket.send(send_data)
        buff = tcp_socket.recv(1024)

        #  4.日志
        LogUtils.log("TCP send to " + str(dest_addr) + '    ' +
                     "Message: " + str(send_data, "utf8") + '    ' +
                     "Back: " + str(buff, "utf8"))

        #  5.关闭套接字
        tcp_socket.close()

        #  6.返回数据
        return buff
    except:
        LogUtils.log("Error:找不到对方" + str(dest_addr))
        return ""
