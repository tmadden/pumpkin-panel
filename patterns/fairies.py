import asyncio
import random

from utilities import *

def neighbors(i):
    n = []
    x, y = index_to_xy(i)
    if x > 0:
        n.append(i - 1)
    if x < y:
        n.append(i + 1)
    width = y + 1
    if y > 0:
        n.append(i - width)
    if y < 5:
        n.append(i + width)
    return n


async def fairies(lights, time_limit):
    background_color = off_color()
    fairy_colors = [
        diverse_palette()[0], warm_white, cold_white
    ]

    for light in lights:
        light.set_state(background_color)

    loop = PeriodicLoop(0.15, time_limit)

    indices = [7, 16, 9]
    while not loop.done():
        for i in range(len(indices)):
            lights[indices[i]].set_state(background_color)
        for i in range(len(indices)):
            indices[i] = random.choice(list(neighbors(indices[i])))
            lights[indices[i]].set_state(fairy_colors[i])
        await loop.next()
