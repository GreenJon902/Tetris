import sys
import time

import pygame

from static_vars import *
from pygame.constants import *


class Block:
    pos = 0, 0

    def __init__(self):
        pass

    def draw(self):
        pass


def draw():
    DISPLAY.fill(background_color)

    for sx in range(horizontal_square_amount):
        x = sx * square_size + sx * square_gap + square_gap

        for sy in range(vertical_square_amount):
            y = sy * square_size + sy * square_gap + square_gap + top_height

            pygame.draw.rect(DISPLAY, square_color, (x, y, square_size, square_size))


    pygame.display.update()


def update_blocks():
    global blocks



pygame.init()

DISPLAY = pygame.display.set_mode(window_size, 0, 32)
pygame.display.set_caption("Tetris - GreenJon902")

blocks: list[Block] = list()
update_timer = 0.0
time_before = time.time()
while True:
    time_after = time.time()
    update_timer += time_after - time_before

    if update_timer >= update_time:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                elif event.key == K_w:
                    pass
                elif event.key == K_a:
                    pass
                elif event.key == K_s:
                    pass
                elif event.key == K_d:
                    pass

        update_blocks()
        update_timer = 0

    time_before = time.time()

    draw()
