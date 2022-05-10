import math
from .color import GREEN, RED, WHITE
import pygame

def percentToAngle(percentage):
    return percentage / 100 * math.pi

def getXYComponents(radius, angle):
    return radius * math.cos(angle), radius * math.sin(angle)

NEEDLE_RADIUS = 75
START = [135, 180]

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
TICK_LABEL_OFFSET_RADIUS = 15
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
        TICK_FONT = pygame.font.SysFont('Comic Sans MS', 17)
        tick_label = TICK_FONT.render(str(percentage), False, WHITE)
        label_x, label_y = getXYComponents(TICK_LABEL_OFFSET_RADIUS, angle)
        tick_label_pos = [
            end[0] - label_x-5,
            end[1] - label_y
        ]
        screen.blit(tick_label, tick_label_pos)
    pygame.draw.line(screen, WHITE, start, end, 3)

def drawModes(screen, curr_mode):
    START_POS = [300, 40]
    SPACING = 60
    modes = ["P", "R", "D", "Power"]
    MODE_FONT = pygame.font.SysFont('Comic Sans MS', 20)
    for i in range(len(modes)):
        mode = modes[i]
        pos = [START_POS[0], START_POS[1]+i*SPACING]
        if mode == "Power":
            pos = [pos[0]-3, pos[1]-5]
            image = pygame.image.load('/home/ctrl/Desktop/CarSimulator/power.png')
            image = pygame.transform.scale(image, (15, 15))
            screen.blit(image, pos)
        else:
            text = MODE_FONT.render(mode, False, GREEN if curr_mode == mode else WHITE)
            screen.blit(text, pos)

def drawTitle(screen):
    TITLE_FONT = pygame.font.SysFont('Comic Sans MS', 30)
    pos = [90, 20]
    text = TITLE_FONT.render('Car Simulator™', False, WHITE)
    screen.blit(text, pos)

def drawDashboard(screen, curr_speed=0, curr_mode="P"):
    pygame.draw.arc(screen, WHITE, [START[0]-100,START[1]-98,200,200], -math.pi/8, 9*math.pi/8, 3)
    for i in range(0, 105, 5):
        drawIntervalTickMark(screen, i, i%10==0)
    drawNeedle(screen, curr_speed)
    drawModes(screen, curr_mode)
    drawTitle(screen)