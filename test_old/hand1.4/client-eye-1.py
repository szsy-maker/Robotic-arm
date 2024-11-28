import pickle
import socket
import RPi.GPIO as GPIO

list_servo = [14, 15, 18, 23, 24, 25]
# GPIO端口号BCM，依次为14,15,18,23,24,25
fPWM = 50  # Hz (PWM方式下的频率，值不能设置过高)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # 去除GPIO警告

for i in list_servo:
    GPIO.setup(i, GPIO.OUT)

# pwm设置
pwm_14 = GPIO.PWM(14, fPWM)
pwm_14.start(0)
pwm_15 = GPIO.PWM(15, fPWM)
pwm_15.start(0)
pwm_18 = GPIO.PWM(18, fPWM)
pwm_18.start(0)
pwm_23 = GPIO.PWM(23, fPWM)
pwm_23.start(0)
pwm_24 = GPIO.PWM(24, fPWM)
pwm_24.start(0)
pwm_25 = GPIO.PWM(25, fPWM)
pwm_25.start(0)

list_pwm = [pwm_14, pwm_15, pwm_18, pwm_23, pwm_24, pwm_25]  # pwm列表
list_max = [140, 180, 180, 180, 180, 180]  # 对应最大角度
list_min = [40, 0, 0, 0, 0, 0]  # 对应最小角度
list_angle = [90, 90, 90, 90, 90, 90]  # 角度集合
data_list = [None for i in range(2)]  # 传输数据集合

n_servo = 0  # 设定舵机
angle_step = 2  # 设定舵机每次调整角度


def math(d):
    return 10 / 180 * d + 2.5


# def angle_change():
#     global n_servo
#     global list_angle
#     global list_max
#     global list_min
#     global data_list
#     global list_angle
#     print(n_servo)
#     print(list_angle)
#     if data_list[6] == 0:
#         list_pwm[n_servo].ChangeDutyCycle(math(list_angle[n_servo]))
#     if data_list[6] == -1:
#         if list_angle[n_servo] > list_min[n_servo]:
#             list_angle[n_servo] -= angle_step
#         list_pwm[n_servo].ChangeDutyCycle(math(list_angle[n_servo]))
#     if data_list[6] == 1:
#         if list_angle[n_servo] < list_max[n_servo]:
#             list_angle[n_servo] += angle_step
#         list_pwm[n_servo].ChangeDutyCycle(math(list_angle[n_servo]))


def right(num):  # 向右角度增加？
    if list_pwm[num] < list_max[num]:
        list_pwm[num] += angle_step


def left(num):
    if list_pwm[num] > list_min[num]:
        list_pwm[num] -= angle_step


def main():
    global n_servo
    global data_list

    host = '192.168.3.250'  # 服务器IP地址 可以在windows上通过ipconfig查找到
    port = 12345  # 服务器端口号
    list_pwm[0].ChangeDutyCycle(math(50))  # 舵机初始化
    client_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)  # 这行代码创建了一个 socket 对象。socket.AF_INET 指定了地址族为 IPv4，socket.SOCK_STREAM 表明这是一个 TCP socket。
    client_socket.connect((host, port))  # 这行代码用之前设置的 IP 地址和端口号来连接服务器。
    while True:
        data = client_socket.recv(1024)
        data_list = pickle.loads(data)
        if data_list[0] == -1:
            left(14)
        elif data_list[0] == 1:
            right(14)
        if data_list[1] == 1:
            left(14)
        elif data_list[1] ==-1:
            right(14)


    # print(data_list)


if __name__ == '__main__':
    main()
    GPIO.cleanup()
