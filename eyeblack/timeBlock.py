import cv2
import numpy as np


def detect_black_blocks_in_video():
    # 初始化摄像头
    cap = cv2.VideoCapture(0)  # 0 表示默认摄像头，如果有多个摄像头，则可能是1, 2等

    while True:
        # 从摄像头读取一帧
        ret, frame = cap.read()

        if not ret:
            print("无法读取帧，请检查摄像头是否正常工作。")
            break

        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 定义黑色的范围（对于灰度图来说，黑色的值通常在0附近）
        lower_black = np.array([0])
        upper_black = np.array([50])  # 可以根据实际情况调整这个阈值

        # 创建一个掩膜，只保留黑色区域
        mask = cv2.inRange(gray, lower_black, upper_black)

        # 查找轮廓
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 遍历每一个轮廓
        for cnt in contours:
            # 获取轮廓的边界框
            x, y, w, h = cv2.boundingRect(cnt)

            # 在原图上画出矩形
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 显示结果
        cv2.imshow('Real-time Black Block Detection', frame)

        # 按 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放摄像头资源并关闭窗口
    cap.release()
    cv2.destroyAllWindows()


# 运行函数
detect_black_blocks_in_video()