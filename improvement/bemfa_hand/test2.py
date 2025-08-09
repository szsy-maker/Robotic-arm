#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

# 创建机械臂对象
Arm = Arm_Device()
time.sleep(.1)
# 同时控制六个舵机运动，逐渐变换角度。
def ctrl_all_servo(angle, s_time = 500):
    Arm.Arm_serial_servo_write6(angle, 180-angle, angle, angle, angle, angle, 
s_time)
    time.sleep(s_time/1000)
def main():
    dir_state = 1
    angle = 90
 
 # 让舵机复位归中
Arm.Arm_serial_servo_write6(90, 90, 90, 90, 90, 90, 500)
time.sleep(1)
 
while True:
    if dir_state == 1:
        angle += 1
    if angle >= 180:
        dir_state = 0
    else:
        angle -= 1
    if angle <= 0:
        dir_state = 1
    
ctrl_all_servo(angle, 10)
time.sleep(10/1000)
# print(angle)
try :
    main()
except KeyboardInterrupt:
     print(" Program closed! ")
     pass

del Arm # 释放掉 Arm 对象