from turtle import left, right
from .motor import Motor

left_motor = Motor(in1=5, in2=6, pwm=26)
right_motor = Motor(in1=21, in2=12, pwm=16)

MAX_SPEED = 100
MIN_SPEED = 0
currSpeed = 0

MAX_ANGLE = 100
MIN_ANGLE = -100
currAngle = 0

def accelerate(amount):
    currSpeed = max(min(MAX_SPEED, currSpeed + amount), MIN_SPEED)
    changeSpeed()

def turn(amount):
    currAngle = max(min(MAX_ANGLE, currAngle + amount), MIN_ANGLE)
    changeSpeed()

def changeSpeed():
    leftSpeed = currSpeed
    rightSpeed = currSpeed
    if currAngle > 0:
        rightSpeed *= 1 - currAngle / 100
    elif currAngle < 0:
        leftSpeed *= 1 + currAngle / 100
    left_motor.change_speed(leftSpeed)
    right_motor.change_speed(rightSpeed)