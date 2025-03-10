import cv2
import numpy as np
import mediapipe as mp
import time
import socket
import pickle
import math

#Initialize

"""
socket通信初始化，若端口号冲突与树莓派段同步修改
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

#全局变量

num = 0
state =False
state_code =True
time_state=True
time_stap_1 =0
time_stap_2 =0
#函数
def socket_sever(message):
    conn.send(message)

#还没写
def identify_state_old():
    global num
    global state
    global state_list
    global pickled_list
    distance_thumb=distance(4,6)
    print(state_list[4])
    if distance_thumb < 70:
        state = True
    elif distance_thumb >100 and state:
        state =False
        #print("yes",num)
        state_list[5]=1
        pickled_list = pickle.dumps(state_list)
        socket_sever(pickled_list)
        state_list[5] = 0
        num +=1

def identify_state():
    global num
    global state
    global state_list
    global pickled_list
    if state_list[5] >180:
        state=True
    elif state_list[5] <165 and state:
        state=False
        #print("yes",num)
        state_list[5]=1
        pickled_list = pickle.dumps(state_list)
        socket_sever(pickled_list)
        state_list[5] = 0
        num +=1
# 测试
def identify_end():
    global  state_code
    global  time_stap_1
    global  time_stap_2
    global  time_state
    if state_list[0]<130 and state_list[1]<130 and state_list[2]< 130 and state_list[3]< 130 and distance(4,7)<50 and time_state:
        time_stap_1=time.time()
        time_state =False
    time_stap_2 =time.time()
    if time_stap_2 -time_stap_1 > 2000:
        print("退出")
        state_code = False

def identify_direction():
    global state_list
    global pickled_list
    if state_list[0] > 165 and state_list[1] > 160 and state_list[2]>160 and state_list[3] > 160:
        state_list[6]=0
    elif  state_list[0]>165 and state_list[1]<90 and state_list[2]<90 and state_list[3]<90:
        state_list[6]=1
    elif state_list[0] <140 and state_list[1] > 160 and state_list[2]>160 and state_list[3] > 160:
        state_list[6]=-1
    print(state_list)

def distance(d1,d2):
    f1 = np.array([RHL.landmark[d1].x * image.shape[1], RHL.landmark[d1].y * image.shape[1]])
    f2 = np.array([RHL.landmark[d2].x * image.shape[1], RHL.landmark[d2].y * image.shape[1]])
    distance_12=math.sqrt(((f1[0]-f2[0])**2)+((f1[0]-f2[0])**2))
    return distance_12

#模型初始化
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

joint_list = [[7, 6, 5], [11, 10, 9], [15, 14, 13], [19, 18, 17],[4,3,2]]  # 手指关节序列
state_list=[0,0,0,0,0,0,0]
#同步记得改7个

#默认摄像头为零
cap = cv2.VideoCapture(0)

with mp_holistic.Holistic(
        model_complexity=1,
        smooth_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.55,) as holistic:
    while cap.isOpened and state_code:
        #time
        start = time.time()

        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            break
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        """
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style())
        """
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                  landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style())
        # 监测到右手，执行
        if results.right_hand_landmarks:
            RHL = results.right_hand_landmarks#缩写
            #test
            #调用函数
            identify_state()
            identify_direction()


            # 计算角度
            for joint in joint_list:
                a = np.array([RHL.landmark[joint[0]].x, RHL.landmark[joint[0]].y])
                b = np.array([RHL.landmark[joint[1]].x, RHL.landmark[joint[1]].y])
                c = np.array([RHL.landmark[joint[2]].x, RHL.landmark[joint[2]].y])
                # 计算弧度
                radians_fingers = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
                angle = np.abs(radians_fingers * 180.0 / np.pi)  # 弧度转角度


                if joint != [4,3,2]:
                    if angle > 180.0:
                        angle = 360 - angle
                state_list[joint_list.index(joint)]=int(angle)
                """
                print(state_list)
                print("食指{}，中指{}，无名指{}，小拇指{}，大拇指{}".format(state_list[0],state_list[1],state_list)[2],state_list[3],state_list[4])

                """
                pickled_list = pickle.dumps(state_list)
                socket_sever(pickled_list)

                cv2.putText(image, str(round(angle, 2)), tuple(np.multiply(b, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                # end
                end = time.time()
                fps = 1 / (end - start)
                fps = "%.2f fps" % fps
                """
                print(fps)
                """



        cv2.imshow('Mediapipe Holistic', image)  # 取消镜面翻转

        if cv2.waitKey(5) == ord('q'):
            break



cap.release()

#手部角度识别