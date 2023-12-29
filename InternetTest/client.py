# -*- coding: utf-8 -*-

import socket

# 创建客户端的 socket 对象 client_socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"  # 设置服务端的 IP 地址
port = 9092  # 设置端口
buf_size = 1024  # 接收套接字的缓冲区大小

# 连接服务端
client_socket.connect((host, port))

# while 循环是为了保证能持续进行对话
while True:
    # 输入发送的消息
    send_msg = input("请输入:")
    # 如果客户端输入的是 q, 则停止对话并且退出程序
    if send_msg == 'q':
        break

    send_msg = send_msg
    # 发送数据, 以二进制的形式发送数据，所以需要进行编码
    client_socket.send(send_msg.encode("utf-8"))
    msg = client_socket.recv(buf_size)
    # 接收服务端返回的数据, 需要解码
    print(msg.decode("utf-8"))

# 关闭客户端
client_socket.close()
