import math
from color import RED, WHITE
import pygame

def percentToAngle(percentage):
    return percentage / 100 * math.pi

def getXYComponents(radius, angle):
    return radius * math.cos(angle), radius * math.sin(angle)

NEEDLE_RADIUS = 75
START = [160, 138]

def drawNeedle(screen, percentage):
    angle = percentToAngle(percentage)
    x, y = getXYComponents(NEEDLE_RADIUS, angle)
    end = [
        START[0] - x,
        START[1] - y
    ]
    pygame.draw.line(screen, RED, START, end, 5)

TICK_MARK_RADIUS = 20
TICK_MARK_OFFSET_RADIUS = 85
TICK_LABEL_OFFSET_RADIUS = 20
def drawIntervalTickMark(screen, percentage, with_label=False):
    angle = percentToAngle(percentage)
    x_offset, y_offset = getXYComponents(TICK_MARK_OFFSET_RADIUS, angle)
    start = [
        START[0] - x_offset,
        START[1] - y_offset
    ]
    x, y = getXYComponents(TICK_MARK_RADIUS, angle)
    end = [
        start[0] - x,
        start[1] - y
    ]
    if with_label:
        TICK_FONT = pygame.font.SysFont('Comic Sans MS', 20)
        tick_label = TICK_FONT.render(str(percentage), False, WHITE)
        label_x, label_y = getXYComponents(TICK_LABEL_OFFSET_RADIUS, angle)
        tick_label_pos = [
            end[0] - label_x-5,
            end[1] - label_y
        ]
        screen.blit(tick_label, tick_label_pos)
    pygame.draw.line(screen, WHITE, start, end, 3)

def drawDashboard(screen, curr_speed):
    pygame.draw.arc(screen, WHITE, [60,40,200,200], -math.pi/8, 9*math.pi/8, 3)
    for i in range(0, 110, 5):
        drawIntervalTickMark(screen, i, i%10==0)
    drawNeedle(screen, curr_speed)