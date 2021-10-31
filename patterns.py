import asyncio
import time

from utilities import *

async def active_pattern(lights):
    for index in range(16):
        lights[(index % 16)].set_state(off)

    loop = PeriodicLoop(1)

    index = 1
    while True:
        lights[(index % 16)].set_state(off)
        index += 1
        lights[(index % 16)].set_state(on)
        await loop.next()

