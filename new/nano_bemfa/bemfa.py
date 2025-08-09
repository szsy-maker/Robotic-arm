import socket
import time


class Connect:
    def __init__(self, uid, topic):
        self.uid = uid
        self.topic = topic
        self.none = None
        self.send = None
        self.tcp_client_socket = None
        self.recvData = None

    def ConnTCP(self):
        # 创建socket

        self.tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # recvData = tcp_client_socket.recv(1024)
        # IP 和端口
        server_ip = 'bemfa.com'
        server_port = 8344
        try:
            # 连接服务器
            self.tcp_client_socket.connect((server_ip, server_port))
        except:
            time.sleep(1)
            self.connTCP()
            print("conn_error")

    def Send_Message(self, msg):
        self.Message = str(msg)
        # 发送
        self.keeplive = 'cmd=2&uid={}&topic={}&msg={}\r\n'.format(self.uid, self.topic, self.Message)
        self.tcp_client_socket.send(self.keeplive.encode("utf-8"))

    def Get_Message(self):
        self.send = 'cmd=1&uid={}&topic={}\r\n'.format(self.uid, self.topic)
        self.tcp_client_socket.send(self.send.encode("utf-8"))

    def extract_msg_param(self, url):
        """
        从URL字符串中提取第三个&后面的msg参数值
        示例: cmd=2&uid=xxx&topic=raspi&msg=5 -> 返回'5'
        """
        parts = url.split('&')
        if len(parts) < 4:
            return None
        msg_part = parts[3]
        if not msg_part.startswith('msg='):
            return None
        return msg_part[4:]

    def Out_put(self):
        self.recvData = self.tcp_client_socket.recv(1024)
        re_str = self.extract_msg_param(self.recvData.decode('utf-8'))
        # print(re_str)
        return re_str


if __name__ == "__main__":
    uid = "0742b4ae2f2c4e1a8ef41a715647bec8"
    topic = "raspi"
    i = 5
    send1 = Connect(uid, topic)
    send1.ConnTCP()

    #测试输出模式
    send1.Get_Message()
    while True:
        print(send1.Out_put())
    #
    # 测试输入模式
    # i = 0
    # while True:
    #     test_list = [0, 1, 2, 3, 4, 5]
    #     i += 1
    #     send1.Send_Message(test_list[i % 6])
    #     time.sleep(1)
