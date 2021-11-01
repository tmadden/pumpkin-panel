import asyncio
import time
import random
from colour import Color

from utilities import *

from operator import add

async def pulsate(lights):
    colors = list(Color("red").range_to(Color("blue"), 6))
    for i in range(4):
        colors.append(colors[-1])
    colors += list(Color("blue").range_to(Color("red"), 6))
    for i in range(4):
        colors.append(colors[-1])

    loop = PeriodicLoop(0.2, 10)

    index = 0
    while not loop.done():
        for light in lights:
            light.set_state(color(colors[index % len(colors)]))
        index += 1
        await loop.next()
