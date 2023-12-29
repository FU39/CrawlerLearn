# -*- coding: utf-8 -*-

import socket

# 创建服务端的 socket 对象 server_socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 7777
buf_size = 1024  # 接收套接字的缓冲区大小

# 绑定地址 (包括 IP 地址和端口号)
server_socket.bind((host, port))
# 设置监听
server_socket.listen(5)

while True:
    # 等待客户端的连接
    # 注意: accept() 函数会返回一个元组, 元素 1 为客户端的 socket 对象, 元素 2 为客户端的地址 (IP地址, 端口号)
    print("Waiting for connection...")
    client_socket, addr = server_socket.accept()
    print("Connected from:", addr)

    # 接收客户端的请求
    data = client_socket.recv(buf_size)
    str_data = data.decode("utf-8")  # 把接收到的数据进行解码
    print("data:", data)
    client_socket.send(
        b"HTTP/1.1 200 ok\r\ncontent-type:text/html\r\n\r\n<h1>alex black girl!</h1><img "
        b"src='https://img0.baidu.com/it/u=4011424408,4733765&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=750'>"
    )
    client_socket.close()

# server_socket.close()
