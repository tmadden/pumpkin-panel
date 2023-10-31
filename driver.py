import yaml
import asyncio
import time
import random
from dataclasses import dataclass

from utilities import reset_all, the_palettes
import utilities

from light import Light

from patterns.connect_four import connect_four
from patterns.progression import progression, transition
from patterns.snake import snake
from patterns.pulsate import pulsate
from patterns.rain import rain
from patterns.twinkle import twinkle
from patterns.fairies import fairies

current_palette_index = 0


async def pattern_rotator(lights, time_Limit=None):

    @dataclass
    class Pattern:
        pattern: ...
        time: float
        starts_blank: bool

    patterns = [
        Pattern(snake, 30, False),
        Pattern(twinkle, 15, False),
        Pattern(rain, 15, False),
        Pattern(fairies, 15, False)
        # Pattern(connect_four, 20, True)
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
            lights, off
            if patterns[active_index].starts_blank else utilities.off_color())


test_pattern = None

pattern_keys = {
    "s": snake,
    "c": connect_four,
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
