import time
import random

from utilities import *

from operator import add


async def snake(lights, time_limit):
    background = off_color()

    head = [0, 0]
    direction = [1, 0]
    snake = []
    just_turned = False

    max_length = 5

    for i in range(24):
        lights[i].set_state(background)

    loop = PeriodicLoop(0.15, time_limit)
    while not loop.done():
        colors = transition_colors()

        if len(snake) >= max_length:
            tail = snake.pop(0)
            lights[index(tail)].set_state(background)

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
            if lights[index(new_head)].get_state() != background:
                continue
            break

        just_turned = not equal(direction, new_direction)

        head, direction = new_head, new_direction
        snake.append(head)

        for i in range(max_length):
            if len(snake) > i and i < len(colors):
                lights[index(snake[-1 - i])].set_state(colors[i],
                                                       seriously=(i < 2))

        await loop.next()
