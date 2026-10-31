from dataclasses import dataclass
import random

from utilities import *


async def embers(lights, time_limit):
    """Palette embers with occasional cold-white sparks (twinkle, show-coherent)."""

    @dataclass
    class State:
        spark: ...  # None or index into a short white flash
        ember_phase: int

    # Spark uses the bright end of the transition ladder
    states = [
        State(spark=None, ember_phase=random.randint(0, 40))
        for _ in range(light_count)
    ]

    loop = PeriodicLoop(0.05, time_limit)
    while not loop.done():
        background = off_color()
        colors = transition_colors()
        spark_seq = [cold_white, cold_white, warm_white] + list(colors[:3])

        for i in range(light_count):
            st = states[i]
            if st.spark is not None:
                if st.spark < len(spark_seq):
                    lights[i].set_state(spark_seq[st.spark], seriously=(st.spark < 2))
                    st.spark += 1
                else:
                    st.spark = None
                    lights[i].set_state(background)
            else:
                # Slow ember: mostly palette off, rare tiny brightening via diverse
                st.ember_phase += 1
                if st.ember_phase % 23 == 0 and random.random() < 0.3:
                    lights[i].set_state(diverse_palette()[0])
                else:
                    lights[i].set_state(background)

        # Launch a few sparks
        if random.random() < 0.35:
            i = random.randint(0, light_count - 1)
            if states[i].spark is None:
                states[i].spark = 0

        for _ in interaction_triggers(0.04):
            for _ in range(2):
                i = random.randint(0, light_count - 1)
                if states[i].spark is None:
                    states[i].spark = 0

        await loop.next()
