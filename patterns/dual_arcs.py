import random

from utilities import *


def _paint_on(lights, pos):
    lights[pos].set_state(on_color_for(pos), seriously=True)
    if is_front(pos):
        outer = back_for(pos)
        if outer is not None:
            lights[outer].set_state(on_color_for(outer))


def _paint_off(lights, pos, background):
    lights[pos].set_state(background)
    if is_front(pos):
        outer = back_for(pos)
        if outer is not None:
            lights[outer].set_state(background)


async def dual_arcs(lights, time_limit):
    """Two short arcs counter-rotate on the front ring (whites on, palette off)."""
    background = off_color()
    for light in lights:
        light.set_state(background)

    seg_len = 3
    a_dir, b_dir = 1, -1
    a_head = random.randrange(front_count)
    b_head = a_head
    for _ in range(front_count // 2):
        b_head = step_front(b_head, 1)

    a_body = []
    b_body = []
    prev = set()

    loop = PeriodicLoop(0.12, time_limit)
    while not loop.done():
        background = off_color()
        for pos in prev:
            _paint_off(lights, pos, background)
        prev.clear()

        a_head = step_front(a_head, a_dir)
        b_head = step_front(b_head, b_dir)
        a_body.append(a_head)
        b_body.append(b_head)
        if len(a_body) > seg_len:
            a_body.pop(0)
        if len(b_body) > seg_len:
            b_body.pop(0)

        active = set(a_body) | set(b_body)
        for pos in active:
            _paint_on(lights, pos)
        prev = set(active)

        await loop.next()
