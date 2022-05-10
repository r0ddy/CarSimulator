import os
from dashboard import drawDashboard
from color import BLACK
from models import mpu
import pygame
import time

# initialize MPU and pygame
steering = mpu.MPU(0x68, 0)
brake = mpu.MPU(0x68, 1)
gas = mpu.MPU(0x69, 1)
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0')
pygame.init()
pygame.mouse.set_visible(False)
size = 320, 240
screen = pygame.display.set_mode(size)

def remake_bounds(zero, hundred):
    def map_val(val):
        if hundred > zero:
            val = min(max(zero, val), hundred)
        else:
            val = max(min(zero, val), hundred)
        diff = abs(hundred - zero)
        return abs(val-zero) / diff * 100
    return map_val
get_steering_percentage = remake_bounds(60, -60)
get_brake_percentage = remake_bounds(-70, -77)
get_gas_percentage = remake_bounds(-69, -87)
while True:
    time.sleep(.1)
    angle = gas.read_x_angle()
    print(angle)
    percentage = get_gas_percentage(angle)
    screen.fill(BLACK)
    drawDashboard(screen, percentage)
    pygame.display.update()
