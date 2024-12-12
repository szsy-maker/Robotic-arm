import cv2
import mediapipe as mp
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hand = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,  # 可以检测的最大手数量
    min_detection_confidence=0.5)  # 最小置信度阈值
cap = cv2.VideoCapture(0)  # 0 表示打开默认摄像头
while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # 将 BGR 图像转换为 RGB。
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 改进性能，可选地将图像标记为不可写。
    image.flags.writeable = False
    results = hands.process(image)

    # 在可视化之前将图像标记回可写状态。
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 绘制手部关键点和连接线。
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:  # 按 ESC 键退出
        break
