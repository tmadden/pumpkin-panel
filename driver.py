import yaml
import asyncio

import requests

from light import Light
from utilities import light_count
from show import control_loop


async def main():
    with open("ips.yml", "r") as file:
        ips = yaml.safe_load(file)

    if len(ips) != light_count:
        raise SystemExit(
            f"ips.yml has {len(ips)} addresses but layout expects "
            f"{light_count} (FRONT_COUNT + backs)")

    lights = [Light(ip) for ip in ips]

    await asyncio.gather(*[light.connect() for light in lights])

    await asyncio.gather(control_loop(lights),
                         *[light.comm_loop() for light in lights])


while True:
    try:
        requests.get("http://192.168.8.1", timeout=1)
        break
    except Exception:
        continue

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
