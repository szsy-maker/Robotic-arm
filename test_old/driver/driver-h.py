import time
import RPi.GPIO as GPIO  # type: ignore

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


class SteppingMotor():
    def __init__(self, name: str, pulse: int, direction: int, step_per_loop: int = 400) -> None:
        r'''
        初始化步进电机类
        (GPIO 接口采用 GPIO.BCM, 基于芯片定义编号)

        参数:
            name: 步进电机名称
            pulse: 对应控制板脉冲+连接的GPIO针脚
            direction: 对应控制板方向+连接的GPIO针脚
            step_per_loop: 控制板设定的细分大小(默认为400)
        '''
        self.name = name
        self.pulse = pulse
        self.direction = direction
        self.step_per_loop = step_per_loop
        GPIO.Setup()
        GPIO.Setup()

    def __setStep__(self, w1, w2) -> None:
        GPIO.output(self.direction, w1)
        GPIO.output(self.pulse, w2)

    def stop(self) -> None:
        r'''停止电机的所有动作'''
        print("Motor " + self.name + " stopping")
        self.__setStep__(0, 0)

    def forward(self, delay: float, steps: int) -> None:
        r'''
        驱动电机前进

        :param delay: 每一步的延时, 以秒为单位（与步进电机的速度成反比）
        :param steps: 前进步数, 见__init__的step_per_loop参数
        '''
        for i in range(0, steps):
            self.__setStep__(1, 1)
            time.sleep(delay)
            self.__setStep__(1, 0)
            time.sleep(delay)

    def backward(self, delay: float, steps: int) -> None:
        r'''
        驱动电机后退

        :param delay: 每一步的延时, 以秒为单位（与步进电机的速度成反比）
        :param steps: 后退步数, 见__init__的step_per_loop参数
        '''
        for i in range(0, steps):
            self.__setStep__(0, 1)
            time.sleep(delay)
            self.__setStep__(0, 0)
            time.sleep(delay)

    def forward_loop(self, delay: float, loops: int) -> None:
        r'''
        驱动电机前进对应圈数

        :param delay: 每一步的延时, 以秒为单位（与步进电机的速度成反比）
        :param loops: 前进圈数, 将会乘以step_per_loop得出最后步数
        '''
        print("Motor " + self.name + " going forward " + str(loops) + " loops, at " + str(delay) + "s per step")
        steps = loops * self.step_per_loop
        self.forward(delay, steps)

    def backward_loop(self, delay: float, loops: int) -> None:
        r'''
        驱动电机后退对应圈数

        :param delay: 每一步的延时, 以秒为单位（与步进电机的速度成反比）
        :param loops: 后退圈数, 将会乘以step_per_loop得出最后步数
        '''
        print("Motor " + self.name + " going backward " + str(loops) + " loops, at " + str(delay) + "s per step")
        steps = loops * self.step_per_loop
        self.backward(delay, steps)

    def destroy(self) -> None:
        GPIO.cleanup((self.pulse, self.direction))

    '''    
    def loop(self):
        while True:
            self.backward(0.0005, 400)
            self.stop()
            time.sleep(1)
            self.forward(0.0005, 400)
            self.stop()
            time.sleep(1)
    '''


class DcMotor():
    def __init__(self, forward: int, backward: int) -> None:
        r'''
        初始化直流电机类
        (GPIO 接口采用 GPIO.BCM, 基于芯片定义编号)

        参数:
            forward: 对应驱动板连接的GPIO针脚
            backward: 对应驱动板接的GPIO针脚
        '''
        self.forward_pin = forward
        self.backward_pin = backward
        GPIO.Setup()
        GPIO.Setup()
        self.__forward = GPIO.PWM(self.forward_pin, 1000)
        self.__backward = GPIO.PWM(self.backward_pin, 1000)
        self.__backward.stop()
        self.__forward.stop()

    def forward(self, speed: int = 100) -> None:
        r'''
        驱动电机前进

        :param speed: 默认为 100， 设置电机前进的速度（0~100）
        '''
        self.__forward.Start()
        self.__backward.stop()

    def backward(self, speed: int = 100) -> None:
        r'''
        驱动电机后退

        :param speed: 默认为 100， 设置电机后退的速度（0~100）
        '''
        self.__backward.Start()
        self.__forward.stop()

    def stop(self) -> None:
        r'''
        停止电机
        '''
        self.__forward.stop()
        self.__backward.stop()


class Servo():

    def __init__(self, control: int) -> None:
        self.control = control
        GPIO.Setup()
        self.pwm = GPIO.PWM(control, 50)
        self.pwm.Start()

    def setDeg(self, deg: int) -> None:
        if isinstance(deg, int):
            self.pwm.ChangeDutyCycle(2.5 + deg * 10 / 180)
        else:
            raise TypeError

    def start(self) -> None:
        self.pwm.Start()

    def stop(self) -> None:
        self.pwm.stop()


class Relay():
    def __init__(self, port):
        self.port = port
        GPIO.Setup()
        GPIO.output(self.port, GPIO.LOW)

    def on(self):
        GPIO.output(self.port, GPIO.HIGH)

    def off(self):
        GPIO.output(self.port, GPIO.LOW)