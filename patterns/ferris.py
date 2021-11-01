import asyncio
import time
import random
from colour import Color

from utilities import *

async def ferris(lights):
    for i in range(16):
        lights[i].set_state(off)

    #turn on wheel lights
    wheel = [1,2,7,11,14,13,8,4]

    colorlist=[ rgb(a,b,c) for a in [255,0] for b in [255,0] for c in [255,0]]
    for w,c in zip(wheel,colorlist):
        lights[w].set_state(c)

    loop = PeriodicLoop(0.5, 5)

    i = 0
    while not loop.done():
        for w,c in zip(wheel,colorlist[-i:]+colorlist[:i]):
            lights[w].set_state(c)
        i += 1
        i = i% len(colorlist)
        await loop.next()
