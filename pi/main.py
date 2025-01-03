import time

import RPi.GPIO as GPIO
from stepdriver import StepDriver
from clinetmodels import Recive

# 舵机GPIO引脚
servo_1 = 12
servo_2 = 16
servo_3 = 20
servo_4 = 21
# 舵机与其他初始化
list_servo = [servo_1, servo_2, servo_3, servo_4]
# GPIO端口号BCM，依次为14,15,18,23,24,25
fPWM = 50  # Hz (PWM方式下的频率，值不能设置过高)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # 去除GPIO警告

for i in list_servo:
    GPIO.setup(i, GPIO.OUT)

# 步进电机引脚
IN1 = 24  # 接PUL-
IN2 = 23  # 接PUL+
IN3 = 22  # 接DIR-
IN4 = 27  # 接DIR+

# 步进电机初始化
step1 = StepDriver(IN1, IN2, IN3, IN4)
step1.setup()

# pwm设置
pwm_1 = GPIO.PWM(servo_1, fPWM)
pwm_1.start(0)
pwm_2 = GPIO.PWM(servo_2, fPWM)
pwm_2.start(0)
pwm_3 = GPIO.PWM(servo_3, fPWM)
pwm_3.start(0)
pwm_4 = GPIO.PWM(servo_4, fPWM)
pwm_4.start(0)

list_pwm = [None, pwm_1, pwm_2, pwm_3, pwm_4]  # pwm列表
list_max = [None, 135, 150, 150, 180]  # 对应最大角度
list_min = [None, 45, 30, 30, 0]  # 对应最小角度
list_angle = [None, 45, 90, 90, 0]  # 角度集合，即为初始设置角度
data_list = [None for i in range(6)]  # 传输数据集合

n_servo = 0  # 设定舵机
angle_step = 2  # 设定舵机每次调整角度


def math_180(d):
    return 10 / 180 * d + 2.5


def math_270(d):
    return 10 / 270 * d + 2.5


def angle_change():
    global n_servo
    global list_angle
    global list_max
    global list_min
    global data_list
    global list_angle
    print(n_servo)
    print(list_angle)
    if n_servo == 0:
        if data_list[6] == -1:
            step1.forward(0.0001, 100)
        if data_list[6] == 1:
            step1.backward(0.0001, 100)
    elif n_servo == 1:
        if data_list[6] == -1:
            if list_angle[n_servo] > list_min[n_servo]:
                list_angle[n_servo] -= angle_step
                list_pwm[n_servo].ChangeDutyCycle(math_270(list_angle[n_servo]))
            else:
                list_pwm[n_servo].ChangeDutyCycle(0)
        elif data_list[6] == 1:
            if list_angle[n_servo] < list_max[n_servo]:
                list_angle[n_servo] += angle_step
                list_pwm[n_servo].ChangeDutyCycle(math_270(list_angle[n_servo]))
            else:
                list_pwm[n_servo].ChangeDutyCycle(0)
        else:
            list_pwm[n_servo].ChangeDutyCycle(0)
    else:
        if data_list[6] == -1:
            if list_angle[n_servo] > list_min[n_servo]:
                list_angle[n_servo] -= angle_step
                list_pwm[n_servo].ChangeDutyCycle(math_180(list_angle[n_servo]))
            else:
                list_pwm[n_servo].ChangeDutyCycle(0)
        elif data_list[6] == 1:
            if list_angle[n_servo] < list_max[n_servo]:
                list_angle[n_servo] += angle_step
                list_pwm[n_servo].ChangeDutyCycle(math_180(list_angle[n_servo]))
            else:
                list_pwm[n_servo].ChangeDutyCycle(0)
        else:
            list_pwm[n_servo].ChangeDutyCycle(0)

def main():
    global n_servo
    global data_list
    client1 = Recive('192.168.3.57', 12345) #填写PC端的ip地址
    client1.Setup()
    while True:
        data_list = client1.Data_List()
        n_servo = data_list[5]
        angle_change()


if __name__ == '__main__':
    list_pwm[1].ChangeDutyCycle(math_270(list_angle[1]))
    for i in range(2, 4):
        list_pwm[i].ChangeDutyCycle(math_180(list_angle[i]))
    time.sleep(2)
    pwm_1.ChangeDutyCycle(0)
    pwm_2.ChangeDutyCycle(0)
    pwm_3.ChangeDutyCycle(0)
    pwm_4.ChangeDutyCycle(0)
    main()
    GPIO.cleanup()
