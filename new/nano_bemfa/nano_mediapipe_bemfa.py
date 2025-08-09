#导入库
import time
from bemfa import Connect
import RPi.GPIO as GPIO
from Arm_Lib import Arm_Device
import ast

def Set_Angle(t):
    for i in list_angle:
        Arm.Arm_serial_servo_write(0, i, t)
        time.sleep(0.01)

def Change_cmd():
    if data_list[0] == "目标":
        pass
    """
    no def
    """

def Change_list():
    global n_servo
    global list_angle
    global list_max
    global list_min
    global data_list
    global list_angle
    print(list_angle,n_servo)
    if data_list[6] ==-1:
        list_angle[n_servo] = max(list_angle[n_servo] -angle_step, list_min)
    if data_list[6] == 1 :
        list_angle[n_servo] = min(list_angle[n_servo] +angle_step, list_max)


def Get_message():
    global data_list
    get_message = send1.Out_put()  ###########
    if type(get_message) == str and get_message != "cmd=2":
        data_list = ast.literal_eval(get_message) #洗干净可以用的列表
        n_servo = data_list[5]

def main():
    global n_servo
    global data_list
    Get_message()
    Change_list()
    Set_Angle(100)

if __name__ == '__main__':
    # 变量
    data_list = [None for i in range(6)]  # 传输数据集合
    list_max = [0, 140, 150, 150, 180,0]  # 对应最大角度
    list_min = [0, 40, 30, 30, 0,0]  # 对应最小角度
    list_angle = [90, 90, 90, 90, 90,90]  # 角度集合，即为初始设置角度

    n_servo = 0  # 设定舵机
    angle_step = 2  # 设定舵机每次调整角度
    # bemfa
    uid = "0742b4ae2f2c4e1a8ef41a715647bec8"
    topic = "raspi"
    i = 5
    send1 = Connect(uid, topic)
    send1.ConnTCP()
    send1.Get_Message()
    # 舵机初始
    Arm = Arm_Device()
    time.sleep(0.1)

    while True:
        main()