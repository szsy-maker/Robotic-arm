import cv2
import numpy as np


def find_black_blocks(image_path):
    # 读取图像
    image = cv2.imread(image_path)

    if image is None:
        print("无法加载图像，请检查路径是否正确。")
        return

    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 打印坐标
        print(f"黑色色块位置: ({x}, {y}) 宽高: {w}x{h}")

    # 显示结果
    cv2.imshow('Detected Black Blocks', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 使用函数
find_black_blocks('black.png')