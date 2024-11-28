import socket
import pickle

# Initialize

"""
socket通信初始化，若端口号冲突与树莓派段同步修改
迭代程序，更快了
"""


class Socket():
    def __init__(self, host, port):
        self.host = host  # 一般默认用“0.0.0.0”
        self.port = port  # 服务器端口号

        # host = '0.0.0.0'  # 监听所有可用的接口
        # port = 12345  # 端口号

    def Setup(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)  # 使服务器开始监听连接请求
        print("等待客户端连接...")
        self.conn, self.address = server_socket.accept()
        print("连接来自: " + str(self.address))
        print(self.conn)

    def Socket_sever(self, message):
        pickled_list = pickle.dumps(message)
        self.conn.send(pickled_list)
