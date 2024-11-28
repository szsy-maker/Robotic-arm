import RPi.GPIO as GPIO
from stepdriver import StepDriver
from clinetmodels import Recive

# '192.168.3.250'
# 接收列表初始化
# 正右 50-130
# 正左 0-60
# 步进电机初始化


# 舵机与其他初始化
list_servo = [16,20,21]
# GPIO端口号BCM，依次为14,15,18,23,24,25
fPWM = 50  # Hz (PWM方式下的频率，值不能设置过高)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # 去除GPIO警告

for i in list_servo:
    GPIO.Setup()

# 步进电机引脚
IN1 = 24  # 接PUL-
IN2 = 23  # 接PUL+
IN3 = 22  # 接DIR-
IN4 = 27  # 接DIR+

step1 = StepDriver(IN1, IN2, IN3, IN4)
step1.setup()

# pwm设置
pwm_16 = GPIO.PWM(16, fPWM)
pwm_16.Start()
pwm_20 = GPIO.PWM(20, fPWM)
pwm_20.Start()
pwm_21 = GPIO.PWM(21, fPWM)
pwm_21.Start()

list_pwm = [None,pwm_16, pwm_20, pwm_21]  # pwm列表
list_max = [None, 60, 130, 180]  # 对应最大角度
list_min = [None, 0, 50,0]  # 对应最小角度
list_angle = [None, 0, 0,]  # 角度集合
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
    if n_servo ==0:
        if data_list[6] == -1:
            step1.forward(0.0001,100)
        if data_list[6] == 1:
            step1.backward(0.0001,100)
    elif n_servo ==3:
        if data_list[6] == 0:
            list_pwm[n_servo].ChangeDutyCycle(math_180(list_angle[n_servo]))
        if data_list[6] == -1:
            if list_angle[n_servo] > list_min[n_servo]:
                list_angle[n_servo] -= angle_step
            list_pwm[n_servo].ChangeDutyCycle(math_180(list_angle[n_servo]))
        if data_list[6] == 1:
            if list_angle[n_servo] < list_max[n_servo]:
                list_angle[n_servo] += angle_step
            list_pwm[n_servo].ChangeDutyCycle(math_180(list_angle[n_servo]))
    else:
        if data_list[6] == 0:
            list_pwm[n_servo].ChangeDutyCycle(math_270(list_angle[n_servo]))
        if data_list[6] == -1:
            if list_angle[n_servo] > list_min[n_servo]:
                list_angle[n_servo] -= angle_step
            list_pwm[n_servo].ChangeDutyCycle(math_270(list_angle[n_servo]))
        if data_list[6] == 1:
            if list_angle[n_servo] < list_max[n_servo]:
                list_angle[n_servo] += angle_step
            list_pwm[n_servo].ChangeDutyCycle(math_270(list_angle[n_servo]))



def main():
    global n_servo
    global data_list
    list_pwm[0].ChangeDutyCycle(math_180(50))  # 舵机初始化
    client1 = Recive('192.168.3.57', 12346)
    client1.Setup()
    while True:
        data_list = client1.Data_List()
        n_servo = data_list[5]
        angle_change()


if __name__ == '__main__':
    main()
    GPIO.cleanup()
