import cv2
import numpy as np
import mediapipe as mp
import math
import bemfa

class Mediapipe():
    def __init__(self, joint_list, state_num, uid, topic):
        self.joint_list = joint_list
        self.state_num = state_num
        self.uid = uid
        self.topic = topic
        #bemfa
        uid = "0742b4ae2f2c4e1a8ef41a715647bec8"
        topic = "raspi"
        self.send1 = bemfa.Connect(uid, topic)
        self.send1.ConnTCP()

    def Setup(self):
        self.state_list = [0, 0, 0, 0, 0, 0, 0]
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hand = mp.solutions.hands
        self.cap = cv2.VideoCapture(0)
        self.state = False

    def identify_state(self):
        if self.state_list[4] > 180:
            self.state = True
        elif self.state_list[4] < 165 and self.state:
            # print("yes",num)
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
                           min_tracking_confidence=0.7,
                           model_complexity=0) as holistic:
            while self.cap.isOpened:
                success, self.image = self.cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    break
                self.image.flags.writeable = False
                self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
                results = holistic.process(self.image)
                self.image.flags.writeable = True
                self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)
                #
                # 监测到右手，执行
                if results.multi_hand_landmarks:
                    self.RHL = results.multi_hand_landmarks[0]  # 缩写
                    self.mp_drawing.draw_landmarks(self.image, self.RHL, self.mp_hand.HAND_CONNECTIONS)
                    # test_old
                    # 计算角度
                    for joint in self.joint_list:
                        a = np.array([self.RHL.landmark[joint[0]].x, self.RHL.landmark[joint[0]].y])
                        b = np.array([self.RHL.landmark[joint[1]].x, self.RHL.landmark[joint[1]].y])
                        c = np.array([self.RHL.landmark[joint[2]].x, self.RHL.landmark[joint[2]].y])
                        # 计算弧度
                        radians_fingers = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
                        angle = np.abs(radians_fingers * 180.0 / np.pi)  # 弧度转角度

                        if joint != [4, 3, 2]:
                            if angle > 180.0:
                                angle = 360 - angle
                        self.state_list[self.joint_list.index(joint)] = int(angle)
                        self.send1.Send_Message(self.state_list)
                        self.identify_state()
                        self.identify_direction()
                        """
                        print(state_list)
                        print("食指{}，中指{}，无名指{}，小拇指{}，大拇指{}".format(state_list[0],state_list[1],state_list)[2],state_list[3],state_list[4])

                        """

                        cv2.putText(self.image, str(round(angle, 2)), tuple(np.multiply(b, [640, 480]).astype(int)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    # end

                cv2.imshow('Mediapipe Holistic', self.image)  # 取消镜面翻转

                if cv2.waitKey(5) == ord('q'):
                    break

        self.cap.release()
