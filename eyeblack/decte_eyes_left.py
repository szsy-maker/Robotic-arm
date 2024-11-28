import cv2
import numpy as np


def detect_left_eye():
    # 初始化摄像头
    cap = cv2.VideoCapture(0)  # 0 表示默认摄像头

    # 加载预训练的人脸和眼睛分类器
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    while True:
        # 从摄像头读取一帧
        ret, frame = cap.read()

        if not ret:
            print("无法读取帧，请检查摄像头是否正常工作。")
            break

        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 检测人脸区域
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (fx, fy, fw, fh) in faces:
            # 在人脸周围画矩形
            cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 2)

            # 在人脸区域内查找眼睛
            roi_gray = gray[fy:fy + fh, fx:fx + fw]
            roi_color = frame[fy:fy + fh, fx:fx + fw]
            eyes = eye_cascade.detectMultiScale(roi_gray)

            left_eye = None
            right_eye = None

            for (ex, ey, ew, eh) in eyes:
                # 计算眼睛中心相对于人脸中心的位置
                center_x = ex + ew // 2
                center_y = ey + eh // 2

                # 假设眼睛位于人脸中心的左侧
                if center_x < fw // 2:
                    left_eye = (ex, ey, ew, eh)
                else:
                    right_eye = (ex, ey, ew, eh)

                # 如果找到了左眼，则跳出循环
                if left_eye is not None:
                    break

            if left_eye:
                # 在左眼周围画矩形
                (ex, ey, ew, eh) = left_eye
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

                # 在眼睛区域内进行进一步的处理
                eye = roi_color[ey:ey + eh, ex:ex + ew]
                eye_gray = roi_gray[ey:ey + eh, ex:ex + ew]

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

                        # 在瞳孔中心画圆圈
                        cv2.circle(eye, (cx, cy), 5, (0, 0, 255), -1)

                # 显示结果
                cv2.imshow('Left Eye Detection', eye)

        # 显示最终结果
        cv2.imshow('Face Detection', frame)

        # 按 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放摄像头资源并关闭窗口
    cap.release()
    cv2.destroyAllWindows()


# 运行函数
detect_left_eye()