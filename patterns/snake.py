import random

from utilities import *


async def snake(lights, time_limit):
    background = off_color()
    colors = transition_colors()
    max_length = min(5, len(colors))

    for light in lights:
        light.set_state(background)

    head = 0
    direction = 1
    body = []

    loop = PeriodicLoop(0.15, time_limit)
    while not loop.done():
        colors = transition_colors()

        if len(body) >= max_length:
            tail = body.pop(0)
            lights[tail].set_state(background)

        candidates = []
        weights = []

        for delta in (-1, 1):
            nxt = step_front(head, delta)
            weight = 10 if delta == direction else 1
            if lights[nxt].get_state() != background:
                weight /= 100
            candidates.append((nxt, delta))
            weights.append(weight)

        outer = back_for(head)
        if outer is not None and lights[outer].get_state() == background:
            candidates.append((outer, direction))
            weights.append(0.5)

        if is_back(head):
            front = front_for_back(head)
            if lights[front].get_state() == background:
                candidates.append((front, direction))
                weights.append(2)

        choice_i = random.choices(range(len(candidates)), weights=weights)[0]
        new_head, new_direction = candidates[choice_i]

        head, direction = new_head, new_direction
        body.append(head)

        for i in range(max_length):
            if len(body) > i and i < len(colors):
                lights[body[-1 - i]].set_state(colors[i], seriously=(i < 2))

        await loop.next()
