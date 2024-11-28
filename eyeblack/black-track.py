import cv2
import numpy as np

# 默认摄像头为零
cap = cv2.VideoCapture(0)


while cap.isOpened :
    success,image=cap.read()
    image_H = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    lowerColor = np.array([0, 0, 0])
    upperColor = np.array([180, 255, 46])
    binary = cv2.inRange(image_H, lowerColor, upperColor)
    median = cv2.medianBlur(binary, 9)# 提取黑色部分（指定区域变黑，其他变黑）

    cv2.imshow('Mediapipe Holistic', median)

    if cv2.waitKey(5) == ord('q'):
        break
# # 2、输出白色色块的二值图并显示
# # 转化为HSV进行处理
# HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# lowerColor = np.array([0, 0, 211])
# upperColor = np.array([180, 30, 255])

# # 提取白色部分（指定区域变白，其他变黑）
# binary = cv2.inRange(HSV, lowerColor, upperColor)

# # 运用中值滤波去除噪声
# median = cv2.medianBlur(binary, 9)
#
# # 显示二值图
# cv2_show('median', median)
#
# # 3、得到轮廓,并在原图输出
# contours, hierachy = cv2.findContours(median, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# res = cv2.drawContours(img, contours, -1, (0, 0, 255), 4)
# cv_show('res', res)
#
# # 4、原图白色中心点
# L = len(contours)  # contours轮廓数据是数组，因此用len()测数组长度，为了循环画点使用
# print("coordinate:")
# for i in range(L):
#     cnt = contours[i]  # cnt表示第i个白色快的轮廓信息
# (x, y), radius = cv2.minEnclosingCircle(cnt)  # 得到白色块外接圆的圆心坐标和半径
# center = (int(x), int(y))  # 画center圆心时。x,y必须是整数
#
# # 标出中心点
# img2 = cv2.circle(img, center, 3, (0, 0, 255), 5)  # 传入圆心信息，并画在原图上
#
# print(center)  # 输出各个中心点
#
# # 显示有中心点的图像
# cv2_show("img2", img2)  # 展示花了中心点的魔方图