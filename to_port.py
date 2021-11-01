# async def active_pattern(lights):
#     next_frame_time = time.perf_counter()
#     for index in range(16):
#         lights[index].set_state(off)
#     while True:
#         lights[0].set_state(255)

#         next_frame_time += 0.1
#         now = time.perf_counter()
#         await asyncio.sleep(next_frame_time - now)

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

# async def active_pattern(lights):
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
#                                                 [0, 1]])
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

# async def active_pattern(lights):
#     next_frame_time = time.perf_counter()
#     index = 0
#     indices = [1, 2, 3, 4]
#     while True:
#         lights[indices.pop(0)].set_state(None)
#         index += 4
#         if index == 19:
#             index = 0
#         if index > 15:
#             index -= 15
#         lights[index].set_state(255)
#         indices.append(index)
#         next_frame_time += 0.1
#         now = time.perf_counter()
#         await asyncio.sleep(next_frame_time - now)


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
