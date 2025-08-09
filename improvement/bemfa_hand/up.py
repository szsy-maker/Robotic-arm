import time
from Arm_Lib import Arm_Device
# 创建机械臂对象
Arm = Arm_Device()
time.sleep(.1)

angel = 30
state = True

Arm.Arm_serial_servo_write(0,90,200)#0是调用所有舵机
#调用这一句,让所有舵机在200ms内转到90°
time.sleep(1)
def Forward(x):
    Arm.Arm_serial_servo_write(1,90,100) #1号舵机在200ms内转到90°
    time.sleep(0.01)
    Arm.Arm_serial_servo_write(2,x,100) #1号舵机在200ms内转到x°
    time.sleep(0.01)
    Arm.Arm_serial_servo_write(3,0,100) #3号舵机在200ms内转到90°
    time.sleep(0.01)
    Arm.Arm_serial_servo_write(4,180-x,100) #4号舵机在200ms内转到180-x°
    time.sleep(0.01)

Forward(30) #意思就是30°倾斜向前伸,可以去看图片

"""
你自己根据案例去设计你想的动作,就跟搭积木一样,有问题我在修,但是你要看程序!!!!
"""

#下面就是循环让他变角度水平前倾,看不懂就别管
while True :
    print(angel)
    if angel <= 30:
        state=True
    elif angel >=70:
        state=False
    else:
        pass
    if state :
        Forward(angel)
        angel +=2
    else:
        Forward(angel)
        angel -=2        


del Arm #释放
