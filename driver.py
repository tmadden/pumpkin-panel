import yaml
import asyncio
import time
import random
from utilities import reset_all

from light import Light

from patterns.connect_four import connect_four
from patterns.progression import progression
from patterns.pulsate import pulsate
from patterns.ramp_up import ramp_up
from patterns.snake import snake

all_patterns = [connect_four, progression, pulsate, ramp_up, snake]

test_pattern = None


async def control_loop(lights):
    if test_pattern:
        await active_pattern(lights)
        reset_all(lights)
        await asyncio.sleep(1)
    else:
        while True:
            for pattern in all_patterns:
                await pattern(lights)


async def main():
    with open("ips.yml", "r") as file:
        ips = yaml.safe_load(file)

    lights = [Light(ip) for ip in ips]

    await asyncio.gather(*[light.connect() for light in lights])

    await asyncio.gather(control_loop(lights),
                         *[light.comm_loop() for light in lights])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
