import random

from utilities import *


async def backbeat(lights, time_limit):
    """Front ring stays palette; outer tier chases / pulses on its own."""
    background = off_color()
    for light in lights:
        light.set_state(background)

    backs = [back_for(f) for f in BACK_OF]
    backs = [b for b in backs if b is not None]
    if not backs:
        loop = PeriodicLoop(0.2, time_limit)
        while not loop.done():
            await loop.next()
        return

    mode = 'chase'  # or 'pulse'
    mode_ticks = 20
    chase_i = 0
    pulse_on = True
    prev = set()

    # Keep fronts on palette
    for i in range(front_count):
        lights[i].set_state(background)

    loop = PeriodicLoop(0.15, time_limit)
    while not loop.done():
        background = off_color()
        for i in range(front_count):
            lights[i].set_state(background)

        mode_ticks -= 1
        if mode_ticks <= 0:
            mode = 'pulse' if mode == 'chase' else 'chase'
            mode_ticks = random.randint(12, 24)

        on_set = set()
        if mode == 'chase':
            chase_i = (chase_i + 1) % len(backs)
            # short trail of 2
            for k in range(min(2, len(backs))):
                on_set.add(backs[(chase_i - k) % len(backs)])
        else:
            pulse_on = not pulse_on
            if pulse_on:
                on_set = set(backs)

        for i in prev - on_set:
            lights[i].set_state(background)
        for i in on_set:
            lights[i].set_state(warm_white, seriously=True)
        prev = on_set

        await loop.next()
