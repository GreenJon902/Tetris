import random
import sys
import time

import pygame

from shapes import shapes, colors as shape_colors
from static_vars import *
from pygame.constants import *


def square_x(x):
    return x * square_size + x * square_gap + square_gap


def square_y(y):
    return y * square_size + y * square_gap + square_gap + top_height


class Block:
    pos = [0, 0]
    shape_id = []

    def __init__(self):
        self.shape_id = random.choice(list(shapes.keys()))

    def draw(self):
        for sy, string in enumerate(shapes[self.shape_id]):
            y = square_y(sy + self.pos[1])
            for sx, pixel_type in enumerate(string):
                x = square_x(sx + self.pos[0])

                if pixel_type != ".":
                    pygame.draw.rect(DISPLAY, shape_colors[self.shape_id], (x, y, square_size, square_size))

    def check_pos(self):
        for sy, string in enumerate(shapes[self.shape_id]):
            y = square_y(sy + self.pos[1])
            for sx, pixel_type in enumerate(string):
                x = square_y(sx + self.pos[0])

                if self.pos[0] + sx < 0:
                    self.pos[0] = 0

                elif self.pos[0] + sx > horizontal_square_amount - 1:
                    self.pos[0] = horizontal_square_amount - len(string)

            if self.pos[1] + sy >= vertical_square_amount:
                self.pos[1] = vertical_square_amount - len(shapes[self.shape_id])
                break



def draw():
    DISPLAY.fill(background_color)

    for sx in range(horizontal_square_amount):
        x = square_x(sx)

        for sy in range(vertical_square_amount):
            y = square_y(sy)

            pygame.draw.rect(DISPLAY, square_color, (x, y, square_size, square_size))


    current_block.draw()
    pygame.display.update()


def update_blocks(block_move_direction):
    global current_block, loops_before_move_down_counter

    if block_move_direction == "l":
        current_block.pos[0] -= 1
    elif block_move_direction == "r":
        current_block.pos[0] += 1


    if loops_before_move_down_counter == loops_before_move_down:
        current_block.pos[1] += 1
        loops_before_move_down_counter = 0
    else:
        loops_before_move_down_counter += 1

    current_block.check_pos()



pygame.init()

DISPLAY = pygame.display.set_mode(window_size, 0, 32)
pygame.display.set_caption("Tetris - GreenJon902")

current_block = Block()
to_move = None
update_timer = 0.0
loops_before_move_down_counter = 0
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

                elif event.key == K_a:
                    to_move = "l"
                elif event.key == K_d:
                    to_move = "r"

            elif event.type == KEYUP:
                to_move = None

        update_blocks(to_move)
        update_timer = 0

    time_before = time.time()

    draw()
