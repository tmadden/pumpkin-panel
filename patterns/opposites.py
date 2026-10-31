import random

from utilities import *


def _slot_pair(offset):
    a = offset % slot_count
    b = (offset + slot_count // 2) % slot_count
    return a, b


def _lights_for_slots(slots):
    result = []
    for slot in slots:
        front = slot_to_front(slot)
        if front is None:
            continue
        result.append(front)
        outer = back_for(front)
        if outer is not None:
            result.append(outer)
    return result


async def opposites(lights, time_limit):
    """Opposite pumpkins rotate; sometimes trail previous pairs into arcs."""
    background = off_color()
    for light in lights:
        light.set_state(background)

    offset = random.randrange(slot_count)
    direction = random.choice([-1, 1])
    trail = 0
    trail_ticks_left = 0
    history = []
    prev_on = set()

    loop = PeriodicLoop(0.09, time_limit)
    while not loop.done():
        background = off_color

        if random.random() < 0.06:
            direction = -direction

        if trail_ticks_left > 0:
            trail_ticks_left -= 1
            if trail_ticks_left == 0:
                trail = 0
        elif random.random() < 0.04:
            trail = random.randint(2, 3)
            trail_ticks_left = random.randint(6, 12)

        offset = (offset + direction) % slot_count
        history.append(_slot_pair(offset))
        keep = trail + 1
        if len(history) > keep:
            history = history[-keep:]

        active_slots = set()
        for a, b in history:
            active_slots.add(a)
            active_slots.add(b)

        on_set = set(_lights_for_slots(active_slots))
        for i in prev_on - on_set:
            lights[i].set_state(background())
        for i in on_set - prev_on:
            lights[i].set_state(on_color_for(i), seriously=True)
        # Refresh colors if still on (palette might be same; cheap no-op)
        for i in on_set & prev_on:
            lights[i].set_state(on_color_for(i))
        prev_on = on_set

        await loop.next()
