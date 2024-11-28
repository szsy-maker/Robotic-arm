import pickle
import socket
class Recive():
    def __init__(self,host,port):
        self.host = host   # 服务器IP地址 可以在windows上通过ipconfig查找到
        self.port =port # 服务器端口号
        data_list=[0,0,0,0,0,0,0]

    def Setup(self):
        self.client_socket = socket.socket(socket.AF_INET,
                                      socket.SOCK_STREAM)  # 这行代码创建了一个 socket 对象。socket.AF_INET 指定了地址族为 IPv4，socket.SOCK_STREAM 表明这是一个 TCP socket。
        self.client_socket.connect((self.host, self.port))  # 这行代码用之前设置的 IP 地址和端口号来连接服务器。

    def Data_List(self):
        data = self.client_socket.recv(1024)
        data_list = pickle.loads(data)
        return data_list
