import random
from dataclasses import dataclass

from utilities import (
    the_palettes, off, off_color, front_count, BACK_OF, set_active_palette,
    on_color_for, rank_bins_ascent, rank_bins_descent, back_for,
)
import utilities

from patterns.progression import progression
from patterns.twinkle import twinkle
from patterns.fairies import fairies
from patterns.dual_arcs import dual_arcs
from patterns.opposites import opposites
from patterns.rank_breathe import rank_breathe
from patterns.rank_fill import rank_fill
from patterns.doorway import doorway
from patterns.entrance import entrance
from patterns.backbeat import backbeat
from patterns.orbit import orbit
from patterns.embers import embers
from patterns.bullets import bullets


current_palette_index = 0


@dataclass
class TransitionOrder:
    """A wipe path plus how many pumpkins stay lit during the wipe."""
    bins: list
    on_count: int


def _backs():
    return [front_count + i for i in range(len(BACK_OF))]


def _as_bins(order):
    return [[i] for i in order]


def _cw_backs_second():
    """Front ring CW, then all backs."""
    return _as_bins(list(range(front_count)) + _backs())


def _ccw_backs_second():
    """Front ring CCW, then backs in reverse."""
    return _as_bins(list(reversed(range(front_count))) + list(reversed(_backs())))


def _cw_paired():
    """CW; each front binned with its back counterpart when present."""
    bins = []
    for i in range(front_count):
        bin_ = [i]
        outer = back_for(i)
        if outer is not None:
            bin_.append(outer)
        bins.append(bin_)
    return bins


def _ccw_paired():
    return list(reversed(_cw_paired()))


# (ordering, how many pumpkins lit in the wipe trail)
transition_orders = [
    TransitionOrder(_cw_backs_second(), on_count=6),
    TransitionOrder(_ccw_backs_second(), on_count=6),
    TransitionOrder(_cw_paired(), on_count=4),
    TransitionOrder(_ccw_paired(), on_count=4),
    TransitionOrder(rank_bins_ascent(include_back=True), on_count=4),
    TransitionOrder(rank_bins_descent(include_back=True), on_count=4),
]


async def transition(lights, order, new_state):
    await progression(
        lights,
        order.bins,
        on_count=order.on_count,
        period=0.1,
        loop=False,
        on_fn=on_color_for,
        off_fn=lambda _i: new_state,
    )
    for light in lights:
        light.set_state(new_state)


async def pattern_rotator(lights, time_limit=None):
    @dataclass
    class Pattern:
        pattern: ...
        time: float
        starts_blank: bool

    patterns = [
        Pattern(embers, 12, False),
        Pattern(dual_arcs, 12, False),
        Pattern(rank_breathe, 12, False),
        Pattern(opposites, 12, False),
        Pattern(entrance, 40, True),
        Pattern(rank_fill, 14, False),
        Pattern(orbit, 14, False),
        Pattern(doorway, 14, False),
        Pattern(backbeat, 10, False),
        Pattern(bullets, 16, True),
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


async def progression_show(lights, time_limit=10):
    await progression(
        lights, rank_bins_ascent(include_back=True),
        on_count=4,
        time_limit=time_limit / 2 if time_limit else None,
        loop=False)
    await progression(
        lights, rank_bins_descent(include_back=True),
        on_count=4,
        time_limit=time_limit / 2 if time_limit else None,
        loop=False)


test_pattern = None

pattern_keys = {
    "t": twinkle,
    "m": embers,
    "f": fairies,
    "d": dual_arcs,
    "o": opposites,
    "r": rank_breathe,
    "l": rank_fill,
    "w": doorway,
    "n": entrance,
    "k": backbeat,
    "b": orbit,
    "u": bullets,
    "p": progression_show,
    "a": pattern_rotator,
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
