from dataclasses import dataclass
import random

from utilities import *


async def rain(lights, time_limit):
    column_states = [None] * 6

    loop = PeriodicLoop(0.15, time_limit)
    while not loop.done():
        colors = transition_colors()

        for i in range(6):
            for j in range(4):
                light = lights[index((i, j))]
                state = column_states[i]
                if state is None:
                    light.set_state(off_color())
                    continue
                if state < j:
                    light.set_state(off_color())
                    continue
                state -= j
                if j < 3:
                    state *= 2
                else:
                    state = int(state / 2)
                if state >= len(colors):
                    light.set_state(off_color())
                    continue
                light.set_state(colors[state], seriously=True)

        active_columns = [i for i in range(6) if column_states[i] is not None]
        for i in active_columns:
            if column_states[i] < 3 + len(colors):
                column_states[i] += 1
            else:
                column_states[i] = None

        for _ in interaction_triggers(0.15):
            available_columns = [
                i for i in range(6) if column_states[i] is None
            ]
            if not available_columns:
                break

            column = random.choice(available_columns)
            column_states[column] = 0

        await loop.next()
