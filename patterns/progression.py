import asyncio
import time
import random
from colour import Color

from utilities import *

from operator import add


async def progression(lights):
    loop = PeriodicLoop(0.1, 10)
    index = 0
    while not loop.done():
        lights[(index - 6) % 24].set_state(off_color())
        lights[index % 24].set_state(on)
        index += 1
        await loop.next()


async def transition(lights, new_state):
    loop = PeriodicLoop(0.1)
    index = 0
    while index < 30:
        if index >= 6:
            lights[index - 6].set_state(new_state)
        if index < 24:
            lights[index % 24].set_state(cold_white)
        index += 1
        await loop.next()
