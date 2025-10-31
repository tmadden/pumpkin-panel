import time
import random

from utilities import *

from operator import add


async def snake(lights, time_limit):
    background = off_color()

    head = (0, 0)
    direction = (0, 1)
    snake = []

    max_length = 5

    for i in range(21):
        lights[i].set_state(background)

    loop = PeriodicLoop(0.15, time_limit)
    while not loop.done():
        colors = transition_colors()

        if len(snake) >= max_length:
            tail = snake.pop(0)
            lights[index(tail)].set_state(background)

        possible_directions = []
        direction_weights = []
        for dir in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1)]:
            weight = 1

            new_head = tuple(map(add, head, dir))
            if not in_bounds(new_head):
                continue

            # Don't turn back on yourself.
            if equal(dir, flipped(direction)):
                continue

            # Prefer to avoid hitting yourself.
            if lights[index(new_head)].get_state() != background:
                weight /= 100
            # Add a bias towards going straight.
            if equal(dir, direction):
                weight *= 10

            possible_directions.append(dir)
            direction_weights.append(weight)
        new_direction = random.choices(possible_directions, weights=direction_weights)[0]
        new_head = tuple(map(add, head, new_direction))

        just_turned = not equal(direction, new_direction)

        head, direction = new_head, new_direction
        snake.append(head)

        for i in range(max_length):
            if len(snake) > i and i < len(colors):
                lights[index(snake[-1 - i])].set_state(colors[i],
                                                       seriously=(i < 2))

        await loop.next()
