from .motor import Motor

left_motor = Motor(in1=5, in2=6, pwm=26)
right_motor = Motor(in1=21, in2=12, pwm=16)

MAX_SPEED = 100
MIN_SPEED = 0
currSpeed = 0

MAX_ANGLE = 100
MIN_ANGLE = -100
currAngle = 0

def init():
    global currSpeed, currAngle
    currSpeed = 0
    currAngle = 0

def accelerate(amount, reverse=False):
    global currSpeed
    currSpeed = max(min(MAX_SPEED, amount), MIN_SPEED)
    changeSpeed(reverse)

def turn(amount, reverse=False):
    global currAngle
    currAngle = max(min(MAX_ANGLE, amount), MIN_ANGLE)
    changeSpeed(reverse)

def changeSpeed(reverse=False):
    global currAngle, currSpeed
    leftSpeed = currSpeed
    rightSpeed = currSpeed
    if currAngle > 0:
        rightSpeed *= 1 - currAngle / 100
    elif currAngle < 0:
        leftSpeed *= 1 + currAngle / 100
    right_motor.change_speed(leftSpeed, reverse)
    left_motor.change_speed(rightSpeed, reverse)

def stop():
    left_motor.set_direction(Motor.STOP)
    right_motor.set_direction(Motor.STOP)