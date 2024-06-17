import socket  
import RPi.GPIO as GPIO 
import time
import pickle


P_SERVO = 18 # GPIO端口号BCM，依次为18、23、24、25 
fPWM = 50 # Hz (PWM方式下的频率，值不能设置过高) 
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)# 去除GPIO警告

GPIO.setup(18, GPIO.OUT) 
pwm = GPIO.PWM(18, fPWM) 
pwm.start(0) 


def math (d):
    return 10 / 180 * d + 2.5


 
pwm.ChangeDutyCycle(math(0))
time.sleep(1.5)


n=0

def main():
    global n
    host = '192.168.3.250'  # 服务器IP地址 可以在windows上通过ipconfig查找到
    port = 12345       # 服务器端口号

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #这行代码创建了一个 socket 对象。socket.AF_INET 指定了地址族为 IPv4，socket.SOCK_STREAM 表明这是一个 TCP socket。
    client_socket.connect((host, port))  #这行代码用之前设置的 IP 地址和端口号来连接服务器。
    pwm.ChangeDutyCycle(n)
    while True:
        data = client_socket.recv(1024)
        data_list=pickle.loads(data)
#        print(data_list)
        if data_list[5]==1:
            print("yes")
        #haimeixie
        if  data_list[6]==0:
            pwm.ChangeDutyCycle(math(n))
        if  data_list[6]==-1:
            if n >0:
                n -=10
            pwm.ChangeDutyCycle(math(n))
        if  data_list[6]==1:
            if n <180:            
                n +=10
            pwm.ChangeDutyCycle(math(n))
            
        print(n)
            
        

#
if __name__ == '__main__':
    main()
    GPIO.cleanup()