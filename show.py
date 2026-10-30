import random
from dataclasses import dataclass

from utilities import (
    PeriodicLoop, the_palettes, off, off_color, cold_white, light_count,
    front_count, BACK_OF, set_active_palette,
)
import utilities

from patterns.progression import progression
from patterns.snake import snake
from patterns.twinkle import twinkle
from patterns.fairies import fairies


current_palette_index = 0


def _unified_cw():
    order = []
    for i in range(front_count):
        order.append(i)
        back = utilities.back_for(i)
        if back is not None:
            order.append(back)
    return order


def _backs():
    return [front_count + i for i in range(len(BACK_OF))]


def _front_cw():
    return list(range(front_count)) + _backs()


def _front_ccw():
    return list(reversed(range(front_count))) + list(reversed(_backs()))


def _front_then_backs_cw():
    return list(range(front_count)) + _backs()


def _backs_then_front_ccw():
    return _backs() + list(reversed(range(front_count)))


def _every_other_cw():
    even = list(range(0, front_count, 2))
    odd = list(range(1, front_count, 2))
    return even + odd + _backs()


transition_orders = [
    _front_cw(),
    _front_ccw(),
    _front_then_backs_cw(),
    _backs_then_front_ccw(),
    _every_other_cw(),
    list(reversed(_every_other_cw())),
]


async def transition(lights, order, new_state):
    n = len(order)
    loop = PeriodicLoop(0.1)
    index = 0
    while index < n + 6:
        if index >= 6:
            lights[order[index - 6]].set_state(new_state)
        if index < n:
            lights[order[index]].set_state(cold_white)
        index += 1
        await loop.next()


async def pattern_rotator(lights, time_limit=None):
    @dataclass
    class Pattern:
        pattern: ...
        time: float
        starts_blank: bool

    patterns = [
        Pattern(twinkle, 15, False),
        Pattern(snake, 20, False),
        Pattern(fairies, 15, False),
    ]
    active_index = 0

    while True:
        active = patterns[active_index]
        await active.pattern(lights, active.time)
        active_index = (active_index + 1) % len(patterns)
        global current_palette_index
        current_palette_index = (current_palette_index + 1) % len(the_palettes)
        set_active_palette(the_palettes[current_palette_index])
        await transition(
            lights, random.choice(transition_orders),
            off if patterns[active_index].starts_blank else off_color())


async def test_progression(lights, time_limit=None):
    order = _unified_cw()
    loop = PeriodicLoop(0.1, time_limit)
    index = 0
    while not loop.done():
        lights[order[(index - 4) % light_count]].set_state(off_color())
        lights[order[index % light_count]].set_state(utilities.on)
        index += 1
        await loop.next()


test_pattern = None

pattern_keys = {
    "s": snake,
    "t": twinkle,
    "f": fairies,
    "a": pattern_rotator,
    "p": progression,
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
