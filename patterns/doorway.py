import random

from utilities import *


async def doorway(lights, time_limit):
    """Entrance edges pulse; occasional white guest walks one side of the ring."""
    background = off_color()
    for light in lights:
        light.set_state(background)

    left = front_count - 1
    right = 0
    guest = None
    guest_dir = 1
    guest_steps_left = 0
    pulse = 0
    cooldown = 8
    prev_extra = set()

    loop = PeriodicLoop(0.12, time_limit)
    while not loop.done():
        background = off_color()
        pulse += 1
        door_on = pulse % 6 < 4

        # Reset previous guest/extras to palette
        for i in prev_extra:
            lights[i].set_state(background)
        prev_extra.clear()

        # Doorway
        for i in (left, right):
            if door_on:
                lights[i].set_state(cold_white, seriously=True)
                outer = back_for(i)
                if outer is not None:
                    lights[outer].set_state(warm_white)
            else:
                lights[i].set_state(background)
                outer = back_for(i)
                if outer is not None:
                    lights[outer].set_state(background)

        # Guest
        if guest is not None:
            guest = step_front(guest, guest_dir)
            guest_steps_left -= 1
            at_back = front_rank(guest) >= rank_count() - 1
            # Don't sit on the doorway forever when wrapping logic fails
            if at_back or guest_steps_left <= 0 or guest in (left, right):
                guest = None
                cooldown = random.randint(10, 18)
            else:
                lights[guest].set_state(cold_white, seriously=True)
                prev_extra.add(guest)
                outer = back_for(guest)
                if outer is not None:
                    lights[outer].set_state(warm_white)
                    prev_extra.add(outer)
        elif cooldown > 0:
            cooldown -= 1
        else:
            guest_dir = random.choice([-1, 1])
            guest = right if guest_dir == 1 else left
            guest = step_front(guest, guest_dir)  # leave the doorway
            guest_steps_left = rank_count() + 2
            lights[guest].set_state(cold_white, seriously=True)
            prev_extra.add(guest)

        # Keep non-door, non-guest fronts on palette
        door_set = {left, right}
        for i in (left, right):
            outer = back_for(i)
            if outer is not None:
                door_set.add(outer)
        for i in range(light_count):
            if i in door_set or i in prev_extra:
                continue
            lights[i].set_state(background)

        await loop.next()
