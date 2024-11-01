import yaml
import asyncio

from pywizlight import discovery


async def main():
    with open("macs.yml", "r") as file:
        macs = yaml.safe_load(file)

    bulbs = await discovery.discover_lights(broadcast_space="192.168.8.255", wait_time=6)

    print(len(bulbs))

    for bulb in bulbs:
        if bulb.mac not in macs:
            print(bulb.mac)

    # print(yaml.dump([(bulb.ip, bulb.mac) for bulb in bulbs]))

    ips = []
    for mac in macs:
        # print(mac)
        ips.append(next(bulb.ip for bulb in bulbs if bulb.mac == mac))

    with open('ips.yml', 'w') as file:
        yaml.dump(ips, file, default_flow_style=False)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
