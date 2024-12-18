"""
这是用来测试的激进程序,
还把远程连接给BAN了
仅用来测试手部识别
"""
import cv2
import numpy as np
import mediapipe as mp
import time
import math
from pcsocket import Socket

class Mediapipe():
    def __init__(self, joint_list, state_num, host, port):
        self.joint_list = [tuple(joint) for joint in joint_list]  # 将每个子列表转换为元组
        self.state_num = state_num
        self.host = host
        self.port = port
        self.angle_history = {joint: [] for joint in self.joint_list}  # 历史角度记录
        self.window_size = 5  # 移动平均窗口大小

    def Setup(self):
        self.state_list = [0, 0, 0, 0, 0, 0, 0]
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hand = mp.solutions.hands
        self.cap = cv2.VideoCapture(0)
        # self.wan1 = Socket(self.host, self.port)
        # self.wan1.Setup()
        self.state = False
        self.e_time=0
        self.time_state = True
        self.time_start_i =0
        self.buffer_time=0.5 #缓冲时间0.5秒

    def identify_state(self):
        if self.state_list[4] > 180:
            self.state = True
        elif self.state_list[4] < 165 and self.state:
            if self.time_state:
                self.time_start_i=time.time()
                self.time_state =False
            self.e_time=time.time()- self.time_start_i
            if self.e_time >self.buffer_time:
                self.time_state=True
                if self.state_list[5] < self.state_num:
                    self.state_list[5] = int(self.state_list[5] + 1)
                else:
                    self.state_list[5] = 0
                self.state = False
        #print(self.e_time)

    def identify_state_o(self):
        if self.state_list[4] > 180:
            self.state = True
        elif self.state_list[4] < 165 and self.state:
            if self.state_list[5] < self.state_num:
                self.state_list[5] = int(self.state_list[5] + 1)
            else:
                self.state_list[5] = 0
            self.state = False

    def identify_direction(self):
        if self.state_list[0] > 165 and self.state_list[1] > 160 and self.state_list[2] > 160 and self.state_list[
            3] > 160:
            self.state_list[6] = 0
        elif self.state_list[0] > 165 and self.state_list[1] < 90 and self.state_list[2] < 90 and self.state_list[
            3] < 90:
            self.state_list[6] = 1
        elif self.state_list[0] < 140 and self.state_list[1] > 160 and self.state_list[2] > 160 and self.state_list[
            3] > 160:
            self.state_list[6] = -1
        print(self.state_list)

    def distance(self, d1, d2):
        f1 = np.array([self.RHL.landmark[d1].x * self.image.shape[1], self.RHL.landmark[d1].y * self.image.shape[1]])
        f2 = np.array([self.RHL.landmark[d2].x * self.image.shape[1], self.RHL.landmark[d2].y * self.image.shape[1]])
        distance_12 = math.sqrt(((f1[0] - f2[0]) ** 2) + ((f1[0] - f2[0]) ** 2))
        return distance_12

    def Start(self):
        with self.mp_hand.Hands(min_detection_confidence=0.7,
                           max_num_hands=1,
                           min_tracking_confidence=0.7) as holistic:
            while self.cap.isOpened:
                start = time.time()
                success, self.image = self.cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    break
                self.image.flags.writeable = False
                self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
                results = holistic.process(self.image)
                self.image.flags.writeable = True
                self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)

                if results.multi_hand_landmarks:
                    self.RHL = results.multi_hand_landmarks[0]
                    self.mp_drawing.draw_landmarks(self.image, self.RHL, self.mp_hand.HAND_CONNECTIONS)

                    for joint in self.joint_list:
                        a = np.array([self.RHL.landmark[joint[0]].x, self.RHL.landmark[joint[0]].y])
                        b = np.array([self.RHL.landmark[joint[1]].x, self.RHL.landmark[joint[1]].y])
                        c = np.array([self.RHL.landmark[joint[2]].x, self.RHL.landmark[joint[2]].y])

                        radians_fingers = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
                        angle = np.abs(radians_fingers * 180.0 / np.pi)

                        if joint != (4, 3, 2):
                            if angle > 180.0:
                                angle = 360 - angle

                        # 添加到历史记录中
                        history = self.angle_history[joint]
                        history.append(angle)
                        if len(history) > self.window_size:
                            history.pop(0)

                        # 计算平均角度
                        smoothed_angle = sum(history) / len(history)
                        self.state_list[self.joint_list.index(joint)] = int(smoothed_angle)

                        self.identify_state()
                        self.identify_direction()
                        # self.wan1.Socket_sever(self.state_list)

                        cv2.putText(self.image, str(round(smoothed_angle, 2)), tuple(np.multiply(b, [640, 480]).astype(int)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                    end = time.time()
                    fps = 1 / (end - start)
                    fps = "%.2f fps" % fps

                    #print(fps)

                cv2.imshow('Mediapipe Holistic', self.image)

                if cv2.waitKey(5) == ord('q'):
                    break

        self.cap.release()



