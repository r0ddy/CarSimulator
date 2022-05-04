import RPi.GPIO as GPIO

# Motor class that wraps GPIO and PWM pins around a nicer speed and direction interface
class Motor:
    FREQ = 50

    # speed
    ZERO = 100 # according to ref guide, IN1=L, IN2=L, PWM=H will stop motor
    HALF = 50 # somewhere between 50 and 75 so fiddle with this number
    FULL = 100

    CCW = "CCW"
    CW = "CW"
    STOP = "STOP"

    def __init__(self, in1, in2, pwm):
        GPIO.setmode(GPIO.BCM)
        self.in1 = in1
        GPIO.setup(self.in1, GPIO.OUT)
        self.in2 = in2
        GPIO.setup(self.in2, GPIO.OUT)
        self.pwm_pin = pwm
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pwm_pin, self.FREQ)
        self.pwm.start(0)
        self.speed = 0
        self.direction = self.STOP

    # change dir
    def set_direction(self, dir):
        if dir == self.CCW:
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.HIGH)
        elif dir == self.CW:
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)
        elif dir == self.STOP:
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.LOW)
    
    # stop pwm
    def StopPWM(self):
        self.pwm.stop()

    def change_speed(self, amount):
        self.speed = max(min(100, self.speed + amount), 0)
        if self.speed == 0:
            self.set_direction(self.STOP)
        else:
            self.set_direction(self.CW)
        self.pwm.ChangeDutyCycle(self.speed)