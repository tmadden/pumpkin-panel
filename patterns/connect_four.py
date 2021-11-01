from dataclasses import dataclass
import random

from utilities import *

async def connect_four(lights):
    active_drops = []
    drop_counts_by_column = [0] * 4

    @dataclass
    class Drop:
        column: int
        row: int
        depth: int
        color: ...

    colors = [{'w': 255}, rgb(255, 0, 0), rgb(255, 0, 255), {'c': 255}]

    loop = PeriodicLoop(0.4)

    counter = 0
    while True:
        active_drops = [drop for drop in active_drops if drop.row < drop.depth]
        for drop in active_drops:
            if drop.row >= 0:
                lights[index((drop.row, drop.column))].set_state(off)
            drop.row += 1
            lights[index((drop.row, drop.column))].set_state(drop.color)

        counter += 1
        if counter % 2:
            available_columns = [i for i in range(4) if drop_counts_by_column[i] < 4]
            if not available_columns:
                break
            column = random.choice(available_columns)
            active_drops.append(Drop(column, -1, 3 - drop_counts_by_column[column], random.choice(colors)))
            drop_counts_by_column[column] += 1

        await loop.next()
