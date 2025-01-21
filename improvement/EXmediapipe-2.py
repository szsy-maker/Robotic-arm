import cv2
import numpy as np
import mediapipe as mp
import time
import math

# Initialize

num = 0
state = False
state_code = True
time_state = True
time_stap_1 = 0
time_stap_2 = 0
state_num = 3

joint_list = [[7, 6, 5], [11, 10, 9], [15, 14, 13], [19, 18, 17], [4, 3, 2]]  # 手指关节序列
state_list = [0, 0, 0, 0, 0, 0, 0]


def identify_state():
    global state
    global state_list
    global pickled_list
    if state_list[4] > 180:
        state = True
    elif state_list[4] < 165 and state:
        # print("yes",num)
        if state_list[5] < state_num:
            state_list[5] = int(state_list[5] + 1)
            print(state_list[5] + 1)
        else:
            state_list[5] = 0
        # pickled_list = pickle.dumps(state_list)
        # socket_sever(pickled_list)
        state = False


# 测试
def identify_end():
    global state_code
    global time_stap_1
    global time_stap_2
    global time_state
    if state_list[0] < 130 and state_list[1] < 130 and state_list[2] < 130 and state_list[3] < 130 and distance(4,
                                                                                                                7) < 50 and time_state:
        time_stap_1 = time.time()
        time_state = False
    time_stap_2 = time.time()
    if time_stap_2 - time_stap_1 > 2000:
        print("退出")
        state_code = False


def identify_direction():
    global state_list
    global pickled_list
    if state_list[0] > 165 and state_list[1] > 160 and state_list[2] > 160 and state_list[3] > 160:
        state_list[6] = 0
    elif state_list[0] > 165 and state_list[1] < 90 and state_list[2] < 90 and state_list[3] < 90:
        state_list[6] = 1
    elif state_list[0] < 140 and state_list[1] > 160 and state_list[2] > 160 and state_list[3] > 160:
        state_list[6] = -1
    print(state_list)


def distance(d1, d2):
    f1 = np.array([RHL.landmark[d1].x * image.shape[1], RHL.landmark[d1].y * image.shape[1]])
    f2 = np.array([RHL.landmark[d2].x * image.shape[1], RHL.landmark[d2].y * image.shape[1]])
    distance_12 = math.sqrt(((f1[0] - f2[0]) ** 2) + ((f1[0] - f2[0]) ** 2))
    return distance_12

# 模型初始化
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hand = mp.solutions.hands


# 默认摄像头为零
cap = cv2.VideoCapture(0)

with mp_hand.Hands(min_detection_confidence=0.7,
                   max_num_hands=1,
                   min_tracking_confidence=0.7) as holistic:
    while cap.isOpened and state_code:
        # time
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
        #
        # 监测到右手，执行
        if results.multi_hand_landmarks:
            #
            RHL = results.multi_hand_landmarks[0]  # 缩写
            mp_drawing.draw_landmarks(image, RHL, mp_hand.HAND_CONNECTIONS)
            # test_old
            # 计算角度
            end = time.time()
            fps = 1 / (end - start)
            fps = "%.2f fps" % fps

            print(fps)

        cv2.imshow('Mediapipe Holistic', image)  # 取消镜面翻转

        if cv2.waitKey(5) == ord('q'):
            break

cap.release()

# 手部角度识别
