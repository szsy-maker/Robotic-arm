import cv2
import numpy as np
import mediapipe as mp
import time
import socket
import pickle
import math

# Initialize

"""
socket通信初始化，若端口号冲突与树莓派段同步修改
迭代程序，更快了
"""
host = '0.0.0.0'  # 监听所有可用的接口
port = 12345  # 端口号
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)  # 使服务器开始监听连接请求
print("等待客户端连接...")
conn, address = server_socket.accept()
print("连接来自: " + str(address))
print(conn)

# 全局变量

num = 0
state = False
state_code = True
time_state = True
time_stap_1 = 0
time_stap_2 = 0
state_num = 5

state_list = [None for i in range(2)]  # 生成空列表

def socket_sever(message):
    conn.send(message)

def detect_eyes_and_direction():
    # 初始化摄像头
    cap = cv2.VideoCapture(0)  # 0 表示默认摄像头

    # 加载预训练的眼睛分类器
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    while True:
        # 从摄像头读取一帧
        success, frame = cap.read()

        if not success:
            print("无法读取帧，请检查摄像头是否正常工作。")
            break

        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 检测眼睛区域
        eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        for (ex, ey, ew, eh) in eyes:
            # 在眼睛区域画矩形
            eye = frame[ey:ey + eh, ex:ex + ew]
            eye_gray = gray[ey:ey + eh, ex:ex + ew]

            # 定义瞳孔的范围（对于灰度图来说，瞳孔的值通常较暗）
            lower_black = np.array([0])
            upper_black = np.array([50])  # 根据实际情况调整这个阈值

            # 创建一个掩膜，只保留瞳孔区域
            mask = cv2.inRange(eye_gray, lower_black, upper_black)

            # 查找瞳孔区域的最大轮廓
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                max_contour = max(contours, key=cv2.contourArea)

                # 计算瞳孔中心点
                M = cv2.moments(max_contour)
                if M["m00"] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])

                    # 判断眼神方向 #调整比值
                    direction = "center"
                    if cx < ew * 0.5:
                        direction += ", left"
                        state_list[0] = -1
                    elif cx > ew * 0.5:
                        direction += ", right"
                        state_list[0] = 1
                    else:
                        state_list[0] = 0

                    if cy < eh * 0.5:
                        direction += ", up"
                        state_list[1] = 1
                    elif cy > eh * 0.5:
                        direction += ", down"
                        state_list[1] = -1
                    else:
                        state_list[1] = 0

                    pickled_list = pickle.dumps(state_list)
                    socket_sever(pickled_list)
                    # 在瞳孔中心画圆圈
                    cv2.circle(eye, (cx, cy), 5, (0, 0, 255), -1)

                    # 打印眼神方向
                    print(f"Eye Direction: {direction}")

            # 在眼睛周围画矩形
            cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)

        # 显示结果
        cv2.imshow('Eye Detection', frame)

        # 按 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放摄像头资源并关闭窗口
    cap.release()
    cv2.destroyAllWindows()


# 运行函数
detect_eyes_and_direction()
