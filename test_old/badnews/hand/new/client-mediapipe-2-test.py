import socket  
import RPi.GPIO as GPIO 
import time
import pickle

list_servo =[14,15,18,23,24,25]
# GPIO端口号BCM，依次为14,15,18,23,24,25
fPWM = 50 # Hz (PWM方式下的频率，值不能设置过高) 
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)# 去除GPIO警告


for i in list_servo:
    GPIO.setup(i, GPIO.OUT)
print(list_pwm)

pwm设置
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

list_pwm=[pwm_14,pwm_15,pwm_18,pwm_23,pwm_24,pwm_25]

n_angle=0
n_servo =0
n_mirror=1

def math (d):
    return 10 / 180 * d + 2.5


def angle_cahnge():
    global n_mirror
    if data_list[6] == 0:
        list_pwm[n_mirror].ChangeDutyCycle(math(n))
    if data_list[6] == -1:
        if n_angle > 0:
            n_angle -= 10
        list_pwm[n_mirror].ChangeDutyCycle(math(n))
    if data_list[6] == 1:
        if n_angle < 180:
            n_angle += 10
        list_pwm[n_mirror].ChangeDutyCycle(math(n))

def main():
    global n_servo
    host = '192.168.3.250'  # 服务器IP地址 可以在windows上通过ipconfig查找到
    port = 12345       # 服务器端口号

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #这行代码创建了一个 socket 对象。socket.AF_INET 指定了地址族为 IPv4，socket.SOCK_STREAM 表明这是一个 TCP socket。
    client_socket.connect((host, port))  #这行代码用之前设置的 IP 地址和端口号来连接服务器。
    pwm.ChangeDutyCycle(n)
    while True:
        data = client_socket.recv(1024)
        data_list=pickle.loads(data)
#        print(data_list)
        if data_list[5] != n_mirror:
            if n_servo < 5:
                n_servo +=1
            else:
                n_servo =0
            
        

#
if __name__ == '__main__':
    main()
    GPIO.cleanup()