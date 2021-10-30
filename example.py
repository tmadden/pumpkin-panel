import yaml
import asyncio
import time
import random

from light import Light


async def main():
    with open("ips.yml", "r") as file:
        ips = yaml.safe_load(file)

    lights = [Light(ip) for ip in ips]

    await asyncio.gather(*[light.connect() for light in lights])

    # await asyncio.gather(*[
    #     light.turn_on(
    #         PilotBuilder(speed=100, rgb=(255, 255, 255), brightness=255))
    #     for light in lights
    # ])

    # await asyncio.gather(
    #     *[light.turn_on(PilotBuilder(rgb=(255, 0, 0))) for light in lights])

    # await asyncio.sleep(2)

    # for i in range(6):
    #     await asyncio.gather(*[
    #         light.turn_on(PilotBuilder(rgb=(255, 0, 0), brightness=255))
    #         for light in lights
    #     ])
    #     # await asyncio.gather(*[
    #     #     light.turn_on(PilotBuilder(speed=100, rgb=(255, 0, 0)))
    #     #     for light in lights
    #     # ])
    #     await asyncio.sleep(0.25)
    #     await asyncio.gather(*[
    #         #light.turn_on(PilotBuilder(rgb=(255, 0, 0), brightness=0))
    #         light.turn_off() for light in lights
    #     ])
    #     # await asyncio.gather(*[
    #     #     light.turn_on(PilotBuilder(speed=100, rgb=(255, 100, 100)))
    #     #     for light in lights
    #     # ])
    #     await asyncio.sleep(0.25)

    # states = [False for light in lights]

    # import datetime
    # print(datetime.datetime.now())

    # colors = [(255, 0, 0), (255, 255, 255)]
    # for i in range(10):
    #     await asyncio.gather(
    #         *[
    #             light.turn_on(PilotBuilder(rgb=colors[i % 2]))
    #             for light in lights
    #         ], asyncio.sleep(0.5))

    # def update_light(light, state):
    #     if state:
    #         return light.turn_on(
    #             PilotBuilder(rgb=(255, 255, 255), brightness=20))
    #     else:
    #         return light.turn_off()
    def index(p):
        return p[1] * 4 + p[0]

    def in_bounds(p):
        return p[0] >= 0 and p[0] < 4 and p[1] >= 0 and p[1] < 4

    def flipped(v):
        return [-v[0], -v[1]]

    import math

    def equal(a, b):
        return round(a[0]) == round(b[0]) and round(a[1]) == round(b[1])

    from operator import add

    # async def control_loop():
    #     next_frame_time = time.perf_counter()
    #     head = [0, 0]
    #     direction = [1, 0]
    #     snake = []
    #     just_turned = False
    #     for i in range(1000):
    #         while True:
    #             if just_turned:
    #                 new_direction = direction
    #                 just_turned = False
    #             else:
    #                 new_direction = random.choice([[-1, 0], [1, 0], [0, -1],
    #                                                [0, 1]])
    #                 if equal(new_direction, flipped(direction)):
    #                     continue
    #             new_head = list(map(add, head, new_direction))
    #             if not in_bounds(new_head):
    #                 continue
    #             if lights[index(new_head)].get_state():
    #                 continue
    #             break

    #         just_turned = not equal(direction, new_direction)

    #         lights[index(head)].set_state(None)
    #         lights[index(new_head)].set_state(100)

    #         head, direction = new_head, new_direction

    #         next_frame_time += 0.5
    #         now = time.perf_counter()
    #         await asyncio.sleep(next_frame_time - now)

    # async def control_loop():
    #     next_frame_time = time.perf_counter()
    #     head = [0, 0]
    #     direction = [1, 0]
    #     snake = []
    #     just_turned = False
    #     for i in range(1000):
    #         while True:
    #             if just_turned:
    #                 new_direction = direction
    #                 just_turned = False
    #             else:
    #                 new_direction = random.choice([[-1, 0], [1, 0], [0, -1],
    #                                                [0, 1]])
    #                 if equal(new_direction, flipped(direction)):
    #                     continue
    #             new_head = list(map(add, head, new_direction))
    #             if not in_bounds(new_head):
    #                 continue
    #             if lights[index(new_head)].get_state():
    #                 continue
    #             break

    #         just_turned = not equal(direction, new_direction)

    #         head, direction = new_head, new_direction
    #         snake.append(head)

    #         for i in range(4):
    #             if len(snake) > i:
    #                 lights[index(snake[-i])].set_state(100)

    #         if len(snake) > 4:
    #             tail = snake.pop(0)
    #             lights[index(tail)].set_state(None)

    #         next_frame_time += 0.15
    #         now = time.perf_counter()
    #         await asyncio.sleep(next_frame_time - now)

    # async def control_loop():
    #     next_frame_time = time.perf_counter()
    #     recent_indices = []

    #     for i in range(1000):
    #         while True:
    #             next_on = random.choice(range(16))
    #             if lights[next_on].get_state():
    #                 continue
    #             else:
    #                 lights[next_on].set_state(True)
    #                 recent_indices.append(next_on)
    #                 break

    #         if len(recent_indices) > 4:
    #             next_off = recent_indices.pop(0)
    #             lights[next_off].set_state(False)

    #         next_frame_time += 0.1
    #         now = time.perf_counter()
    #         await asyncio.sleep(next_frame_time - now)
    # async def control_loop():
    #     next_frame_time = time.perf_counter()
    #     index = 0
    #     while True:
    #         lights[index].set_state(None)
    #         index += 4
    #         if index == 19:
    #             index = 0
    #         if index > 15:
    #             index -= 15
    #         lights[index].set_state(100)
    #         next_frame_time += 0.1
    #         now = time.perf_counter()
    #         await asyncio.sleep(next_frame_time - now)
    async def control_loop():
        next_frame_time = time.perf_counter()
        index = 0
        while True:
            lights[index % 16].set_state(100)
            lights[(index - 4) % 16].set_state(80)
            lights[(index - 5) % 16].set_state(50)
            lights[(index - 6) % 16].set_state(20)
            lights[(index - 7) % 16].set_state(None)
            index += 1
            next_frame_time += 0.1
            now = time.perf_counter()
            await asyncio.sleep(next_frame_time - now)

    # async def control_loop():
    #     next_frame_time = time.perf_counter()
    #     while True:
    #         lights[0].set_state(100)
    #         await asyncio.sleep(0.1)
    #         lights[0].set_state(80)
    #         await asyncio.sleep(0.1)
    #         lights[0].set_state(60)
    #         await asyncio.sleep(0.1)
    #         lights[0].set_state(40)
    #         await asyncio.sleep(0.1)
    #         lights[0].set_state(None)
    #         next_frame_time += 0.845
    #         now = time.perf_counter()
    #         await asyncio.sleep(next_frame_time - now)
    async def reset_loop():
        for light in lights:
            light.set_state(None)
        await asyncio.sleep(1)

    try:
        await asyncio.wait_for(
            asyncio.gather(control_loop(),
                           *[light.comm_loop() for light in lights]), 20)
    except asyncio.TimeoutError:
        pass

    try:
        await asyncio.wait_for(
            asyncio.gather(reset_loop(),
                           *[light.comm_loop() for light in lights]), 1)
    except asyncio.TimeoutError:
        pass

    # print(datetime.datetime.now())

    # await asyncio.sleep(1)

    # await asyncio.gather(*[light.turn_off() for light in lights])

    # # Turn on the light into "rhythm mode"
    #
    # # Set bulb brightness
    # await light.turn_on(PilotBuilder(brightness=255))

    # # Set bulb brightness (with async timeout)
    # timeout = 10
    # await asyncio.wait_for(light.turn_on(PilotBuilder(brightness=255)),
    #                        timeout)

    # # Set bulb to warm white
    # await light.turn_on(PilotBuilder(warm_white=255))

    # # Set RGB values
    # # red to 0 = 0%, green to 128 = 50%, blue to 255 = 100%
    # await light.turn_on(PilotBuilder(rgb=(0, 128, 255)))

    # # Get the current color temperature, RGB values
    # state = await light.updateState()
    # print(state.get_colortemp())
    # red, green, blue = state.get_rgb()
    # print(f"red {red}, green {green}, blue {blue}")

    # # Start a scene
    # await light.turn_on(PilotBuilder(scene=4))  # party

    # # Get the name of the current scene
    # state = await light.updateState()
    # print(state.get_scene())

    # # # Get the features of the bulb
    # bulb_type = await lights[0].get_bulbtype()
    # print(bulb_type.features.brightness
    #       )  # returns true if brightness is supported
    # print(bulb_type.features.color)  # returns true if color is supported
    # print(bulb_type.features.color_tmp
    #       )  # returns true if color temperatures are supported
    # print(bulb_type.features.effect)  # returns true if effects are supported
    # print(bulb_type.kelvin_range.max)  # returns max kelvin in in INT
    # print(bulb_type.kelvin_range.min)  # returns min kelvin in in INT
    # print(bulb_type.name)  # returns the module name of the bulb

    # # Turns the light off
    # await light.turn_off()

    # Do operations on multiple lights parallely
    #bulb1 = wizlight("<your bulb1 ip>")
    #bulb2 = wizlight("<your bulb2 ip>")
    #await asyncio.gather(bulb1.turn_on(PilotBuilder(brightness = 255)),
    #    bulb2.turn_on(PilotBuilder(warm_white = 255)), loop = loop)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
