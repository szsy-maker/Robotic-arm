import cv2
import matplotlib.pyplot as plt
import mediapipe as mp
import time
import numpy as np

list=[[15,13,11]]

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

colorclass = plt.cm.ScalarMappable(cmap='jet')
colors = colorclass.to_rgba(np.linspace(0, 1, int(33)))
colormap = (colors[:, 0:3])

#teat
def angle(v1,v2,v3):
    X_ = results.pose_landmarks.landmark[v1].x * image.shape[0]
    Y_ = results.pose_landmarks.landmark[v1].y * image.shape[1]
    z_ = results.pose_landmarks.landmark[v1].z * 100
    p1= np.array([X_, Y_, z_])
    X_ = results.pose_landmarks.landmark[v2].x * image.shape[0]
    Y_ = results.pose_landmarks.landmark[v2].y * image.shape[1]
    z_ = results.pose_landmarks.landmark[v2].z * 100
    p2= np.array([X_, Y_, z_])
    X_ = results.pose_landmarks.landmark[v3].x * image.shape[0]
    Y_ = results.pose_landmarks.landmark[v3].y * image.shape[1]
    z_ = results.pose_landmarks.landmark[v3].z * 100
    p3= np.array([X_, Y_, z_])
    v_1 = p1 - p2
    v_2 = p3 - p2
    cos_angle = np.dot(v_1, v_2) / (np.linalg.norm(v_1) * np.linalg.norm(v_2))
    angle = np.arccos(cos_angle)

    # 将弧度转换为度数
    angle =np.degrees(angle)
    print(angle)



def draw3d(plt, ax, world_landmarks, connnection=mp_pose.POSE_CONNECTIONS):
    ax.clear()
    ax.set_xlim3d(-1, 1)
    ax.set_ylim3d(-1, 1)
    ax.set_zlim3d(-1, 1)

    landmarks = []
    for index, landmark in enumerate(world_landmarks.landmark):
        landmarks.append([landmark.x, landmark.z, landmark.y * (-1)])
    landmarks = np.array(landmarks)

    ax.scatter(landmarks[:, 0], landmarks[:, 1], landmarks[:, 2], c=np.array(colormap), s=50)
    for _c in connnection:
        ax.plot([landmarks[_c[0], 0], landmarks[_c[1], 0]],
                [landmarks[_c[0], 1], landmarks[_c[1], 1]],
                [landmarks[_c[0], 2], landmarks[_c[1], 2]], 'k')

    plt.pause(0.001)


# 端口号一般是0，除非你还有其他摄像头
# 使用本地视频推理，复制其文件路径代替端口号即可
cap = cv2.VideoCapture(0)
with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        model_complexity=1) as pose:
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection="3d")

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        start = time.time()
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        #test

        #test
        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        end = time.time()
        fps = 1 / (end - start)
        fps = "%.2f fps" % fps
        # 实时显示帧数
        image = cv2.flip(image, 1)
        cv2.putText(image, "FPS {0}".format(fps), (100, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 3)

        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
        if results.pose_world_landmarks:
            draw3d(plt, ax, results.pose_world_landmarks)

        angle(15,13,11)

cap.release()
