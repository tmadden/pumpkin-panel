import random

from utilities import *


async def fairies(lights, time_limit):
    background_color = off_color()
    fairy_colors = [
        diverse_palette()[0], warm_white, cold_white
    ]

    for light in lights:
        light.set_state(background_color)

    loop = PeriodicLoop(0.15, time_limit)

    # Spread starting points around the front ring
    indices = [
        0,
        front_count // 3,
        (2 * front_count) // 3,
    ]
    while not loop.done():
        for i in range(len(indices)):
            lights[indices[i]].set_state(background_color)
        for i in range(len(indices)):
            indices[i] = random.choice(neighbors(indices[i]))
            lights[indices[i]].set_state(fairy_colors[i])
        await loop.next()
