import time
import random

from utilities import *

from operator import add

async def ramp_up(lights):
    for index in range(16):
        lights[(index % 16)].set_state(off)

    loop = PeriodicLoop(0.5)

    indices = [15, 11, 7, 3]

    for index in range(16):
        count = index % 5
        for i in range(4):
            if i < count:
                lights[indices[i]].set_state(on)
            else:
                lights[indices[i]].set_state(off)
        await loop.next()
