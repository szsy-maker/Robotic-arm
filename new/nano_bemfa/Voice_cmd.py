# 导入库
import time
from Arm_Lib import Arm_Device

class Action_Map():
    def __init__(self,Arm):
        self.Arm = Arm

    def Forward(self,x,t):
        self.Arm.Arm_serial_servo_write(1,90,t) #1号舵机在200ms内转到90°
        time.sleep(0.01)
        self.Arm.Arm_serial_servo_write(2,x,t) #1号舵机在200ms内转到x°
        time.sleep(0.01)
        self.Arm.Arm_serial_servo_write(3,0,t) #3号舵机在200ms内转到90°
        time.sleep(0.01)
        self.Arm.Arm_serial_servo_write(4,180-x,t) #4号舵机在200ms内转到180-x°
        time.sleep(0.01)

    def Init(self,x,t):
        self.Arm.Arm_serial_servo_write(0,x,t) #全部复位


if __name__ =="__main__":
    Action_Map.Init()