import asyncio
import time
import random
from colour import Color

from utilities import *

from operator import add

def _unified_cw():
    order = []
    for i in range(front_count):
        order.append(i)
        back = back_for(i)
        if back is not None:
            order.append(back)
    return order

async def progression(lights, time_limit=10):
    order = _unified_cw()
    loop = PeriodicLoop(0.1, time_limit)
    index = 0
    while not loop.done():
        lights[order[(index - 6) % len(order)]].set_state(off_color())
        lights[order[index % len(order)]].set_state(on)
        index += 1
        await loop.next()
