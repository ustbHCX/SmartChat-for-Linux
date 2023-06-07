import socket


def connect(dest_host: str, dest_port: int, send_data: bytes):
    #  1.建立套接字socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # AF_INET表示使用ipv4,SOCK_DGRAM表示使用UDP通信协议

    #  2.发送数据
    udp_socket.sendto(send_data, (dest_host, dest_port))  # 编码成全球统一数据格式，用元组表示接收方ip和port

    #  3.关闭套接字
    udp_socket.close()


def listen():
    #  1.建立套接字socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # AF_INET表示使用ipv4,SOCK_DGRAM表示使用UDP通信协议

    #  2.绑定端口port
    local_addr = ("127.0.0.1", 53521)  # 默认本机任何ip ，指定端口号53521
    udp_socket.bind(local_addr)  # 绑定端口

    while True:
        #  3.接收数据
        recv_data = udp_socket.recvfrom(1024)  # 定义单次最大接收字节数

        #  4.返回数据
        recv_msg = recv_data[0]  # 接收的元组形式的数据有两个元素，第一个为发送信息
        recv_addr = recv_data[1]  # 元组第二个元素为发信息方的ip以及port
        print(recv_msg, "from", recv_addr)
        # return recv_msg, recv_addr

        if not recv_data:
            break

    #  5.关闭套接字
    udp_socket.close()
