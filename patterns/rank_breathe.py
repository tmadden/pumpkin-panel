from utilities import *


async def rank_breathe(lights, time_limit):
    """Tide: ranks light white then fall back to palette, sweeping up and down."""
    background = off_color()
    for light in lights:
        light.set_state(background)

    bins = ranks(include_back=True)
    n = len(bins)
    if n == 0:
        return

    # rank index along a ping-pong path
    path = list(range(n)) + list(range(n - 2, 0, -1))
    path_i = 0
    prev = set()

    loop = PeriodicLoop(0.18, time_limit)
    while not loop.done():
        background = off_color()
        active_rank = path[path_i % len(path)]
        on_set = set(bins[active_rank])

        for i in prev - on_set:
            lights[i].set_state(background)
        for i in on_set:
            lights[i].set_state(on_color_for(i), seriously=True)
        prev = on_set

        path_i += 1
        await loop.next()
