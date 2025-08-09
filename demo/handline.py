import cv2
import numpy as np
import mediapipe as mp
import matplotlib.pyplot as plt
import time

# 模型初始化
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hand = mp.solutions.hands

joint_list = [[7, 6, 5], [11, 10, 9], [15, 14, 13], [19, 18, 17], [4, 3, 2]]
state_list = [0, 0, 0, 0, 0, 0, 0]
indices = [0,5, 9, 13,17,0]
list_x=[None for i in range(20)]
list_y=[None for i in range(20)]
list_z=[None for i in range(20)]
# 默认摄像头为零
cap = cv2.VideoCapture(0)

#3d
def pot_3d(x,y,z):
    ax1.set_xlim3d(-1, 1)
    ax1.set_ylim3d(-1, 1)
    ax1.set_zlim3d(-1, 1)
    ax1.clear()
    ax1.scatter(x,y,z,marker='o', s=100)
    ax1.plot(x[:5],y[:5],z[:5])
    ax1.plot(x[5:9],y[5:9],z[5:9])
    ax1.plot(x[9:13],y[9:13],z[9:13])
    ax1.plot(x[13:17],y[13:17],z[13:17])
    ax1.plot(x[17:20],y[17:20],z[17:20])
    ax1.plot([x[i] for i in indices],[y[i] for i in indices],[z[i] for i in indices])
    plt.pause(0.001)

with mp_hand.Hands(model_complexity=0) as holistic:
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1,projection = "3d")
    while cap.isOpened:
        start =time.time()
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            break
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 监测到右手，执行
        if results.multi_hand_landmarks:
            RHL = results.multi_hand_landmarks[0]  # 缩写
            mp_drawing.draw_landmarks(image, RHL, mp_hand.HAND_CONNECTIONS)
            # test
            # 计算角度
            for joint in joint_list:
                a = np.array([RHL.landmark[joint[0]].x, RHL.landmark[joint[0]].y])
                b = np.array([RHL.landmark[joint[1]].x, RHL.landmark[joint[1]].y])
                c = np.array([RHL.landmark[joint[2]].x, RHL.landmark[joint[2]].y])
                # 计算弧度
                radians_fingers = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
                angle = np.abs(radians_fingers * 180.0 / np.pi)  # 弧度转角度

                if joint != [4, 3, 2]:
                    if angle > 180.0:
                        angle = 360 - angle
                state_list[joint_list.index(joint)] = int(angle)
                for i in range(20):
                    list_x[i] =RHL.landmark[i].x
                    list_y[i] =RHL.landmark[i].y
                    list_z[i] =RHL.landmark[i].z
                pot_3d(list_x,list_y,list_z)


                #print(RHL.landmark[4].x,RHL.landmark[4].y,RHL.landmark[4].z*-1)

                #print(state_list)
                #print("食指{}，中指{}，无名指{}，小拇指{}，大拇指{}".format(state_list[0],state_list[1],state_list)[2],state_list[3],state_list[4])

                cv2.putText(image, str(round(angle, 2)), tuple(np.multiply(b, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            # end
            end = time.time()
            fps = 1 / (end - start)
            fps = "%.2f fps" % fps

            #print(fps)

        cv2.imshow('Mediapipe Holistic', image)  # 取消镜面翻转

        if cv2.waitKey(5) == ord('q'):
            break

cap.release()
