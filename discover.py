import yaml
import asyncio

from pywizlight import discovery


async def main():
    with open("macs.yml", "r") as file:
        macs = yaml.safe_load(file)

    bulbs = await discovery.discover_lights(broadcast_space="192.168.11.255")

    ips = [next(bulb.ip for bulb in bulbs if bulb.mac == mac) for mac in macs]

    with open('ips.yml', 'w') as file:
        yaml.dump(ips, file, default_flow_style=False)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
