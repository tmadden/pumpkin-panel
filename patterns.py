import asyncio
import time
import random

from utilities import *

from operator import add

async def ramp_up(lights):
    for index in range(16):
        lights[(index % 16)].set_state(off)

    loop = PeriodicLoop(0.5)

    indices = [15, 11, 7, 3]

    index = 0
    while True:
        count = index % 5
        index += 1
        for i in range(4):
            if i < count:
                lights[indices[i]].set_state(on)
            else:
                lights[indices[i]].set_state(off)
        await loop.next()

async def snake(lights):
    head = [0, 0]
    direction = [1, 0]
    snake = []
    just_turned = False

    loop = PeriodicLoop(0.25)

    while True:
        while True:
            if just_turned:
                new_direction = direction
                just_turned = False
            else:
                new_direction = random.choice([[-1, 0], [1, 0], [0, -1],
                                                [0, 1]])
                if equal(new_direction, flipped(direction)):
                    continue
            new_head = list(map(add, head, new_direction))
            if not in_bounds(new_head):
                continue
            if lights[index(new_head)].get_state():
                continue
            break

        just_turned = not equal(direction, new_direction)

        head, direction = new_head, new_direction
        snake.append(head)

        for i in range(4):
            if len(snake) > i:
                lights[index(snake[-i])].set_state(100)

        if len(snake) > 4:
            tail = snake.pop(0)
            lights[index(tail)].set_state(None)

        await loop.next()

active_pattern = snake
