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
        Pattern(rain, 15, False),
        Pattern(twinkle, 15, False),
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


# from pynput import keyboard, mouse

# mouse_controller = mouse.Controller()

# last_right_click_time = 0

# def on_move(x, y):
#     utilities.mouse_position[0] += x
#     utilities.mouse_position[1] += y
#     if [x, y] != [0, 0]:
#         mouse_controller.position = (0, 0)

# def on_click(x, y, button, pressed):
#     global last_right_click_time
#     global current_palette_index

#     current_time = time.time()

#     if pressed:
#         if button == mouse.Button.left:
#             utilities.mouse_clicks.append(button)
#             utilities.record_interaction()
#         elif button == mouse.Button.right:
#             time_since_last_right_click = current_time - last_right_click_time
#             if time_since_last_right_click < 0.3:
#                 current_palette_index = 0
#             else:
#                 current_palette_index = (current_palette_index +
#                                          1) % len(the_palettes)
#             utilities.set_active_palette(the_palettes[current_palette_index])

#             last_right_click_time = current_time

# mouse_listener = mouse.Listener(on_move=on_move,
#                                 on_click=on_click,
#                                 suppress=True)
# mouse_listener.start()

# def on_press(key):
#     try:
#         if key.char in pattern_keys:
#             current_pattern = pattern_keys[key.char]
#             interrupt_pattern_loop = True
#         if key.char == "a":
#             utilities.reset_interaction()
#     except AttributeError:
#         pass

# keyboard_listener = keyboard.Listener(on_press=on_press)
# keyboard_listener.start()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
