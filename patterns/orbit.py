import random

from utilities import *


async def orbit(lights, time_limit):
    """Cold-white planet orbits the front ring; outer 'moon' fades via transition palette."""
    background = off_color()
    for light in lights:
        light.set_state(background)

    planet = random.randrange(front_count)
    direction = random.choice([-1, 1])
    # moon: back light index → step into transition_colors
    moons = {}  # back_i -> fade_index

    loop = PeriodicLoop(0.14, time_limit)
    while not loop.done():
        background = off_color()
        colors = transition_colors()

        # Clear previous planet
        lights[planet].set_state(background)

        if random.random() < 0.03:
            direction = -direction

        planet = step_front(planet, direction)
        lights[planet].set_state(cold_white, seriously=True)

        # Birth a moon when passing a backed pumpkin
        outer = back_for(planet)
        if outer is not None:
            moons[outer] = 0  # reset / start fade from bright end
            lights[outer].set_state(warm_white, seriously=True)

        # Advance moons through transition palette toward dim/off
        finished = []
        for back_i, idx in list(moons.items()):
            if back_i == outer:
                continue  # just spawned / refreshed
            idx += 1
            if idx >= len(colors):
                lights[back_i].set_state(background)
                finished.append(back_i)
            else:
                # Walk transition colors from bright toward darker end
                lights[back_i].set_state(colors[idx])
                moons[back_i] = idx
        for back_i in finished:
            del moons[back_i]

        # Palette off for idle fronts (planet already set)
        for i in range(light_count):
            if i == planet or i in moons:
                continue
            if lights[i].get_state() != background:
                lights[i].set_state(background)

        await loop.next()
