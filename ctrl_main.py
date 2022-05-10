import os
import pygame
import time
from controller.dashboard import drawDashboard
from controller.color import BLACK
from models.mpu import MPU
import RPi.GPIO as GPIO

# initialize MPU and pygame
steering = MPU(0x68, 0)
brake = MPU(0x68, 1)
gas = MPU(0x69, 1)
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0')
pygame.init()
pygame.mouse.set_visible(False)
size = 320, 240
screen = pygame.display.set_mode(size)

# map bounds on acceloremeter angles to percentage
def remake_bounds(zero, hundred):
    def map_val(val):
        if hundred > zero:
            val = min(max(zero, val), hundred)
        else:
            val = max(min(zero, val), hundred)
        diff = abs(hundred - zero)
        return abs(val-zero) / diff * 100
    return map_val

# maps steering from (0 to 100) to (-100, 100)
def turn(steering_p):
    min_bound = -100
    return steering_p/100 * 200 + min_bound

# determiens the current acceleration
def accelerate(brake_p, gas_p):
    # gas - brake - friction
    return gas_p / 100 - brake_p / 200 - .15

# bound mappers for each accelerometer
get_steering_percentage = remake_bounds(60, -60)
get_brake_percentage = remake_bounds(-70, -77)
get_gas_percentage = remake_bounds(-69, -87)

# state variables
speed = 0
mode = "P"

def park(channel):
    global mode
    mode = "P"

def reverse(channel):
    global mode
    mode = "R"

def drive(channel):
    global mode
    mode = "D"

def power(channel):
    global mode, on
    mode = "Power"
    on = not on
    if on:
        mode = "P"

button_cb_map = {
    17: park,
    22: reverse,
    23: drive,
    27: power
}
GPIO.setmode(GPIO.BCM)
for pin in button_cb_map:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_cb_map[pin], bouncetime=300)

on = True

while True:
    time.sleep(.1)
    if on:
        gas_a = gas.read_x_angle()
        gas_p = get_gas_percentage(gas_a)
        brake_a = brake.read_x_angle()
        brake_p = get_brake_percentage(brake_a)
        steering_a = steering.read_x_angle()
        steering_p = get_steering_percentage(steering_a)
        
        if mode == "P":
            speed = 0
        else:
            speed = min(max(accelerate(brake_p, gas_p)+speed, 0), 100)
        screen.fill(BLACK)
        drawDashboard(screen, speed, mode)
    else:
        screen.fill(BLACK)
    pygame.display.update()
