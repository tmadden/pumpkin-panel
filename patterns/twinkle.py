from dataclasses import dataclass
import asyncio
import time
import random
from colour import Color

from utilities import *

from operator import add


async def twinkle(lights, time_limit):

    @dataclass
    class State:
        twinkle_index: ...
        background_index: int

    states = [
        State(twinkle_index=None, background_index=random.randint(0, 119))
        for _ in range(24)
    ]

    loop = PeriodicLoop(0.02, time_limit)
    while not loop.done():
        transitions = transition_colors()
        diversity = diverse_palette()

        for i in range(24):
            state = states[i]
            if state.twinkle_index is not None and state.twinkle_index < len(
                    transitions) * 3:
                lights[i].set_state(transitions[int(state.twinkle_index / 6)])
                state.twinkle_index += 1
            else:
                state.twinkle_index = None
                lights[i].set_state(diversity[state.background_index %
                                              len(diversity)])

        states[random.randint(0, 23)].background_index = random.randint(0, 119)

        for _ in interaction_triggers(0.05):
            for _ in range(3):
                index = random.randint(0, 23)
                if states[index].twinkle_index is None:
                    states[index].twinkle_index = 0

        await loop.next()
