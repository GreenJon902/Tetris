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
    pos = list(block_start_pos)
    shape_id = []
    rotation = 0

    def __init__(self):
        self.shape_id = random.choice(list(shapes.keys()))
        self.rotation = random.randint(0, 3)

    def draw(self):
        for sy, string in enumerate(shapes[self.shape_id][self.rotation]):
            y = square_y(sy + self.pos[1])
            for sx, pixel_type in enumerate(string):
                x = square_x(sx + self.pos[0])

                if pixel_type != ".":
                    pygame.draw.rect(DISPLAY, shape_colors[self.shape_id], (x, y, square_size, square_size))

    def check_pos(self, block_move_direction):
        global current_block

        for sy, string in enumerate(shapes[self.shape_id][self.rotation]):
            for sx, pixel_type in enumerate(string):
                try:
                    if pixel_type == "o" and dormant_bricks[sx + self.pos[0]][sy + self.pos[1] + 1] != ".":
                        if block_move_direction == "l":
                            current_block.pos[0] += 1
                        elif block_move_direction == "r":
                            current_block.pos[0] -= 1

                        else:  # Hitting because fell on block
                            self.make_dormant()
                            print("Creating new block")
                            current_block = Block()
                            current_block.pos = [0, 0]
                            break

                except IndexError:  # Most likely because bottom or top layer
                    pass

                if self.pos[0] + sx < 0:
                    self.pos[0] = 0

                elif self.pos[0] + sx > horizontal_square_amount - 1:
                    self.pos[0] = horizontal_square_amount - len(string)

            if self.pos[1] + sy >= vertical_square_amount - 1:
                self.pos[1] = vertical_square_amount - len(shapes[self.shape_id][self.rotation])

                self.make_dormant()
                print("Creating new block")
                current_block = Block()
                current_block.pos = [0, 0]
                break

    def make_dormant(self):
        for sy, string in enumerate(shapes[self.shape_id][self.rotation]):
            y = sy + self.pos[1]
            for sx, pixel_type in enumerate(string):
                x = sx + self.pos[0]

                if pixel_type != ".":
                    dormant_bricks[x][y] = self.shape_id


def draw():
    DISPLAY.fill(background_color)

    for sx in range(horizontal_square_amount):
        x = square_x(sx)

        for sy in range(vertical_square_amount):
            y = square_y(sy)

            pygame.draw.rect(DISPLAY, square_color, (x, y, square_size, square_size))

    for sx, x_colors in enumerate(dormant_bricks):
        x = square_x(sx)
        for sy, color in enumerate(x_colors):
            y = square_y(sy)

            if color != ".":
                pygame.draw.rect(DISPLAY, shape_colors[color], (x, y, square_size, square_size))

    current_block.draw()
    pygame.display.update()


def update_blocks(block_move_direction):
    global current_block, loops_before_move_down_counter

    if block_move_direction == "l":
        current_block.pos[0] -= 1

    elif block_move_direction == "r":
        current_block.pos[0] += 1

    elif block_move_direction == "d":
        current_block.pos[1] += 1


    if loops_before_move_down_counter >= loops_before_move_down and block_move_direction != "d":
        current_block.pos[1] += 1
        loops_before_move_down_counter = 0

    else:
        loops_before_move_down_counter += 1

    current_block.check_pos(block_move_direction)

    # Loosing
    for x in dormant_bricks:
        if x[0] != ".":
            print("Player lost!")
            pygame.quit()
            sys.exit()

    # Line destroy
    for sy, y_colors in enumerate(zip(*dormant_bricks[::-1])):
        if "." not in y_colors:
            for sx in dormant_bricks:
                sx.pop(sy)
                sx.insert(0, ".")


pygame.init()

DISPLAY = pygame.display.set_mode(window_size, 0, 32)
pygame.display.set_caption("Tetris - GreenJon902")

current_block = Block()
to_move = None
update_timer = 0.0
loops_before_move_down_counter = 0
time_before = time.time()
dormant_bricks = [["." for y in range(vertical_square_amount)] for x in range(horizontal_square_amount)]
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
                elif event.key == K_s:
                    to_move = "d"
                elif event.key == K_r:
                    current_block.rotation = (current_block.rotation + 1) % 4

            elif event.type == KEYUP:
                to_move = None

        update_blocks(to_move)
        update_timer = 0

    time_before = time.time()

    draw()
