# 树莓派python程序中不能出现汉字，需要把注释中的汉字换成英文

import RPi.GPIO as GPIO
import time

#sw Microstep 8 Pulse 1600 Current 3.0 PK 3.2
# 规定GPIO引脚
IN1 = 18  # 接PUL-
IN2 = 16  # 接PUL+
IN3 = 15  # 接DIR-
IN4 = 13  # 接DIR+


def setStep(w1, w2, w3, w4):
    GPIO.output(IN1, w1)
    GPIO.output(IN2, w2)
    GPIO.output(IN3, w3)
    GPIO.output(IN4, w4)


def stop():
    setStep(0, 0, 0, 0)


def forward(delay, steps):
    for i in range(0, steps):
        setStep(1, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(1, 0, 0, 1)
        time.sleep(delay)


def backward(delay, steps):
    for i in range(0, steps):
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(1, 0, 1, 0)
        time.sleep(delay)


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
    GPIO.Setup()  # Set pin's mode is output
    GPIO.Setup()
    GPIO.Setup()
    GPIO.Setup()


def loop():
    while True:
        print("backward...")
        backward(0.001, 100)  # 发射脉冲时间间隔0.0001（单位秒）   脉冲个数1000

        print("stop...")
        stop()  # stop
        time.sleep(0.1)  # sleep 3s

        print("forward...")
        #forward(0.0001, 500)

        print("stop...")
        stop()
        time.sleep(0.1)

def loop_q(x):
    for i in range(x):
        backward(0.0001, 100)
        time.sleep(0.01)
  

def destroy():
    GPIO.cleanup()  # 释放数据


if __name__ == '__main__':  # Program start from here
    setup()
    try:
        loop_q(10)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child function destroy() will be  executed.
        destroy()
