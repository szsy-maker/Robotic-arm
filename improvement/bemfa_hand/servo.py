#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device
# 创建机械臂对象
Arm = Arm_Device()
time.sleep(.1)
for i in range(50):
    Arm.Arm_serial_servo_write(3,180,200)
    time.sleep(0.1)

del Arm # 释放掉 Arm 对象