from dataclasses import dataclass
import random

from utilities import *


async def plinko(lights, time_limit):
    active_drops = []

    @dataclass
    class Drop:
        x: int
        y: int
        color: ...

    colors = [{'w': 255}, {'c': 255}]

    for light in lights:
        light.set_state(off_color())

    loop = PeriodicLoop(0.35)

    counter = 0
    while True:
        drops = []
        for drop in active_drops:
            possible_moves = [(drop.x, drop.y + 1), (drop.x + 1, drop.y + 1)]
            moves = [move for move in possible_moves if in_bounds(move) and lights[index(move)].get_state() == off_color()]
            if len(moves) == 0:
                continue
            lights[index((drop.x, drop.y))].set_state(off_color(), seriously=True)
            drop.x, drop.y = random.choice(moves)
            lights[index((drop.x, drop.y))].set_state(drop.color)
            drops.append(drop)
        active_drops = drops.copy()

        counter += 1
        if counter % 3 == 0:
            if lights[0].get_state() == off_color():
                color = colors[counter // 3 % len(colors)]
                lights[0].set_state(color)
                active_drops.append(Drop(0, 0, color))
            else:
                break

        await loop.next()
