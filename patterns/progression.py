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
        lights[(index - 6) % light_count].set_state(off_color())
        lights[index % light_count].set_state(on)
        index += 1
        await loop.next()

