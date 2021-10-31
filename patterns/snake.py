import time
import random

from utilities import *

from operator import add

async def snake(lights):
    head = [0, 0]
    direction = [1, 0]
    snake = []
    just_turned = False

    loop = PeriodicLoop(0.25, 20)

    while not loop.done():
        if len(snake) > 4:
            tail = snake.pop(0)
            lights[index(tail)].set_state(off)

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

        if len(snake) > 0:
            lights[index(snake[-1])].set_state(rgb(0, 0, 255))
        if len(snake) > 1:
            lights[index(snake[-2])].set_state(rgb(120, 120, 255))
        if len(snake) > 2:
            lights[index(snake[-3])].set_state(rgb(255, 255, 255))
        if len(snake) > 3:
            lights[index(snake[-4])].set_state(rgb(255, 255, 255))

        await loop.next()
