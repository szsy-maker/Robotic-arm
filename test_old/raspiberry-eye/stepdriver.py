import RPi.GPIO as GPIO
import time


# sw Microstep 8 Pulse 1600 Current 3.0 PK 3.2
# 规定GPIO引脚

class StepDriver():
    def __init__(self, IN1, IN2, IN3, IN4):
        self.IN1 = IN1
        self.IN2 = IN2
        self.IN3 = IN3
        self.IN4 = IN4

    def setStep(self, w1, w2, w3, w4):
        GPIO.output(self.IN1, w1)
        GPIO.output(self.IN2, w2)
        GPIO.output(self.IN3, w3)
        GPIO.output(self.IN4, w4)

    def stop(self):
        self.setStep(0, 0, 0, 0)

    def forward(self,delay, steps):
        for i in range(0, steps):
            self.setStep(1, 0, 1, 0)
            time.sleep(delay)
            self.setStep(0, 1, 1, 0)
            time.sleep(delay)
            self.setStep(0, 1, 0, 1)
            time.sleep(delay)
            self.setStep(1, 0, 0, 1)
            time.sleep(delay)

    def backward(self,delay, steps):
        for i in range(0, steps):
            self.setStep(1, 0, 0, 1)
            time.sleep(delay)
            self.setStep(0, 1, 0, 1)
            time.sleep(delay)
            self.setStep(0, 1, 1, 0)
            time.sleep(delay)
            self.setStep(1, 0, 1, 0)
            time.sleep(delay)

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by physical location
        GPIO.Setup()  # Set pin's mode is output
        GPIO.Setup()
        GPIO.Setup()
        GPIO.Setup()

    def test_step(self):
        while True:
            print("backward...")
            self.backward(0.0001, 500)  # 发射脉冲时间间隔0.0001（单位秒）   脉冲个数1000

            print("stop...")
            self.stop()  # stop
            time.sleep(0.1)  # sleep 3s

            print("forward...")
            self.forward(0.0001, 500)

            print("stop...")
            self.stop()
            time.sleep(0.1)

    def destroy(self):
        GPIO.cleanup()  # 释放数据
