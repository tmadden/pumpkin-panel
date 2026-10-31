from utilities import *


async def rank_fill(lights, time_limit):
    """Fill ranks entrance→back with white, hold, then drain back→entrance."""
    background = off_color()
    for light in lights:
        light.set_state(background)

    bins = ranks(include_back=True)
    n = len(bins)
    if n == 0:
        return

    filled = 0  # number of ranks currently lit (from entrance)
    filling = True
    hold_ticks = 0

    loop = PeriodicLoop(0.16, time_limit)
    while not loop.done():
        background = off_color()

        if hold_ticks > 0:
            hold_ticks -= 1
        elif filling:
            filled += 1
            if filled >= n:
                filled = n
                filling = False
                hold_ticks = 4
        else:
            filled -= 1
            if filled <= 0:
                filled = 0
                filling = True
                hold_ticks = 3

        on_set = set()
        for r in range(filled):
            on_set.update(bins[r])

        for i in range(light_count):
            if i in on_set:
                lights[i].set_state(on_color_for(i), seriously=True)
            else:
                lights[i].set_state(background)

        await loop.next()
