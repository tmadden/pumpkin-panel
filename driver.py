import yaml
import asyncio
import time
import random

from light import Light

from patterns import active_pattern

async def main():
    with open("ips.yml", "r") as file:
        ips = yaml.safe_load(file)

    lights = [Light(ip) for ip in ips]

    await asyncio.gather(*[light.connect() for light in lights])

    try:
        await asyncio.wait_for(
            asyncio.gather(active_pattern(lights),
                           *[light.comm_loop() for light in lights]), 20)
    except asyncio.TimeoutError:
        pass

    async def reset_loop():
        for light in lights:
            light.set_state(None)
        await asyncio.sleep(1)

    try:
        await asyncio.wait_for(
            asyncio.gather(reset_loop(),
                           *[light.comm_loop() for light in lights]), 1)
    except asyncio.TimeoutError:
        pass


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
