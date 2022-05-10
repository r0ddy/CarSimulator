import os
from calc import drawDashboard, drawIntervalTickMark, drawNeedle
from color import BLACK
import pygame
import time
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0')

pygame.init()
pygame.mouse.set_visible(False)
size = 320, 240
screen = pygame.display.set_mode(size)
screen.fill(BLACK)
drawDashboard(screen, 50)
pygame.display.update()
time.sleep(3)