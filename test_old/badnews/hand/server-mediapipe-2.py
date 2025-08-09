import cv2
import numpy as np
import mediapipe as mp
import time
import socket
import pickle

#Initialize
host = '0.0.0.0'  # 监听所有可用的接口
port = 12345  # 端口号
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))

server_socket.listen(1)  # 使服务器开始监听连接请求
print("等待客户端连接...")
conn, address = server_socket.accept()
print("连接来自: " + str(address))
print(conn)

def socket_sever(message):
    conn.send(message)

#还没写
def identify_hand():
    None





#模型初始化
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

joint_list = [[7, 6, 5], [11, 10, 9], [15, 14, 13], [19, 18, 17]]  # 手指关节序列
angle_list=[0,0,0,0]#同步记得改

cap = cv2.VideoCapture(0)
with mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            break
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
        #                           landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style())
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                  landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style())
        # 监测到右手，执行
        if results.right_hand_landmarks:
            RHL = results.right_hand_landmarks
            # 计算角度
            for joint in joint_list:
                a = np.array([RHL.landmark[joint[0]].x, RHL.landmark[joint[0]].y])
                b = np.array([RHL.landmark[joint[1]].x, RHL.landmark[joint[1]].y])
                c = np.array([RHL.landmark[joint[2]].x, RHL.landmark[joint[2]].y])
                # 计算弧度
                radians_fingers = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
                angle = np.abs(radians_fingers * 180.0 / np.pi)  # 弧度转角度


                if angle > 180.0:
                    angle = 360 - angle
                angle_list[joint_list.index(joint)]=int(angle)
                print(angle_list)
                print("食指{}，中指{}，无名指{}，小拇指{}".format(angle_list[0],angle_list[1],angle_list[2],angle_list[3]))
                pickled_list = pickle.dumps(angle_list)
                socket_sever(pickled_list)
                time.sleep(0.01)#不知道需不需要留着吧

                cv2.putText(image, str(round(angle, 2)), tuple(np.multiply(b, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        #cv2.imshow('MediaPipe Holistic', cv2.flip(image, 1))
        cv2.imshow('Mediapipe Holistic', image)  # 取消镜面翻转



        if cv2.waitKey(5) == ord('q'):
            break



cap.release()

#手部角度识别