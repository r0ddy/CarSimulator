import os
import pygame
import time
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0')
BLACK = 0,0,0
pygame.init()
size = width, height = 320, 240
screen = pygame.display.set_mode(size)
screen.fill(BLACK)

Pi = 3.14
pygame.draw.arc(screen, (255,255,255), [50,50,50,50], Pi/2, Pi, 2)

time.sleep(5)