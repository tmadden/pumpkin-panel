import yaml
import asyncio
import time
import random
from dataclasses import dataclass

from utilities import reset_all, the_palettes, on, off, off_color, PeriodicLoop, light_count, cold_white
import utilities

from light import Light

from patterns.plinko import plinko
from patterns.progression import progression
from patterns.snake import snake
# from patterns.pulsate import pulsate
from patterns.rain import rain
from patterns.twinkle import twinkle
from patterns.fairies import fairies

current_palette_index = 0

linear_1f = list(range(light_count))
linear_1r = list(reversed(linear_1f))
linear_2f = [
    0, 1, 3, 6, 10, 15, 16, 11, 7, 4, 2, 5, 8, 18, 17, 18, 13, 9, 14, 19, 20
]
linear_2r = list(reversed(linear_2f))
circular_order_1f = [
    0, 1, 3, 6, 10, 15, 16, 17, 18, 19, 20, 14, 9, 5, 2, 4, 7, 11, 12, 13, 8
]
circular_order_1r = list(reversed(circular_order_1f))
circular_order_2f = [
    20, 14, 9, 5, 2, 0, 1, 3, 6, 10, 15, 16, 17, 18, 19, 13, 8, 4, 7, 11, 12
]
circular_order_2r = list(reversed(circular_order_2f))
transition_orders = [
    linear_1f, linear_1r, linear_2f, linear_2r, circular_order_1f,
    circular_order_1r, circular_order_2f, circular_order_2r
]


async def transition(lights, order, new_state):
    loop = PeriodicLoop(0.1)
    index = 0
    while index < light_count + 6:
        if index >= 6:
            lights[order[index - 6]].set_state(new_state)
        if index < light_count:
            lights[order[index]].set_state(cold_white)
        index += 1
        await loop.next()


async def pattern_rotator(lights, time_Limit=None):
    @dataclass
    class Pattern:
        pattern:...
        time: float
        starts_blank: bool

    patterns = [
        Pattern(twinkle, 15, False),
        Pattern(snake, 20, False),
        Pattern(fairies, 15, False),
        Pattern(plinko, 0, False)
    ]
    active_index = 0

    while True:
        active = patterns[active_index]
        await active.pattern(lights, active.time)
        active_index = (active_index + 1) % len(patterns)
        global current_palette_index
        current_palette_index = (current_palette_index + 1) % len(the_palettes)
        utilities.set_active_palette(the_palettes[current_palette_index])
        await transition(
            lights, random.choice(transition_orders), off
            if patterns[active_index].starts_blank else utilities.off_color())


async def test_progression(lights, time_limit=None):
    order = circular_order_2
    loop = PeriodicLoop(0.1, time_limit)
    index = 0
    while not loop.done():
        lights[order[(index - 4) % light_count]].set_state(off_color())
        lights[order[index % light_count]].set_state(on)
        index += 1
        await loop.next()


test_pattern = None

pattern_keys = {
    "s": snake,
    "p": plinko,
    "r": rain,
    "t": twinkle,
    "a": pattern_rotator
}

current_pattern = pattern_rotator


async def control_loop(lights):
    global current_pattern

    while True:
        utilities.interrupt_pattern_loop = False
        utilities.mouse_clicks.clear()
        if test_pattern:
            await test_pattern(lights, None)
        else:
            await current_pattern(lights, None)


async def main():
    with open("ips.yml", "r") as file:
        ips = yaml.safe_load(file)

    lights = [Light(ip) for ip in ips]

    await asyncio.gather(*[light.connect() for light in lights])

    await asyncio.gather(control_loop(lights),
                         *[light.comm_loop() for light in lights])


import requests

while True:
    try:
        requests.get("http://192.168.8.1", timeout=1)
        break
    except:
        continue

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
