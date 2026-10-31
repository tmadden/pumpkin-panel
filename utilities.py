import asyncio
import math
import time
import random
from dataclasses import dataclass

try:
    from pywizlight.rgbcw import rgb2rgbcw
except ImportError:
    # Visualizer / offline use — rgb() falls back to plain RGB
    def rgb2rgbcw(rgb_tuple):
        return rgb_tuple, None


mouse_position = [0, 0]


def mouse():
    return mouse_position


mouse_clicks = []


def clicks():
    new_clicks = mouse_clicks.copy()
    mouse_clicks.clear()
    return new_clicks


last_interaction_time = None


def reset_interaction():
    global last_interaction_time
    last_interaction_time = None


def record_interaction():
    global last_interaction_time
    last_interaction_time = time.time()


def user_is_interacting():
    return last_interaction_time and time.time() - last_interaction_time < 10


def interaction_triggers(probability):
    if user_is_interacting():
        return clicks()
    else:
        if random.random() < probability:
            return [()]
        else:
            return []


# Circle layout: N front pumpkins, M virtual entrance slots, optional outer backs.
# lights[0 .. N-1] = front ring (CW from just after the entrance)
# lights[N .. N+B-1] = outer tier, parallel to BACK_OF front indices
# Tweak these for the physical setup; total should match ips.yml length.
FRONT_COUNT = 16  # N
ENTRANCE_SLOTS = 3  # M
BACK_OF = [0, 5, 10, 15]  # front indices with a pumpkin outside them

front_count = FRONT_COUNT
entrance_slots = ENTRANCE_SLOTS
slot_count = FRONT_COUNT + ENTRANCE_SLOTS
light_count = FRONT_COUNT + len(BACK_OF)


def is_front(light_i):
    return 0 <= light_i < FRONT_COUNT


def is_back(light_i):
    return FRONT_COUNT <= light_i < light_count


def back_for(front_i):
    """Light index of the outer pumpkin behind front_i, or None."""
    try:
        return FRONT_COUNT + BACK_OF.index(front_i)
    except ValueError:
        return None


def front_for_back(light_i):
    """Front index paired with a back-tier light."""
    return BACK_OF[light_i - FRONT_COUNT]


def light_to_slot(light_i):
    if is_front(light_i):
        return light_i
    return front_for_back(light_i)


def slot_to_front(slot):
    """Front light index for an occupied slot, or None for the entrance."""
    if 0 <= slot < FRONT_COUNT:
        return slot
    return None


def slot_occupied(slot):
    return slot_to_front(slot) is not None


def step_front(front_i, delta):
    """Move ±1 (or more) along the front ring, skipping the entrance arc."""
    slot = light_to_slot(front_i)
    for _ in range(slot_count):
        slot = (slot + delta) % slot_count
        front = slot_to_front(slot)
        if front is not None:
            return front
    raise RuntimeError("no front pumpkins")


def front_neighbors(front_i):
    return [step_front(front_i, -1), step_front(front_i, 1)]


def neighbors(light_i):
    """Adjacent lights for effects: ring neighbors, plus front/back pairs."""
    result = []
    if is_front(light_i):
        result.extend(front_neighbors(light_i))
        outer = back_for(light_i)
        if outer is not None:
            result.append(outer)
    else:
        result.append(front_for_back(light_i))
    return result


def slot_theta(slot):
    """Math angle (CCW from +x); entrance arc centered at the bottom."""
    mid_entrance = FRONT_COUNT + (ENTRANCE_SLOTS - 1) / 2.0
    return 1.5 * math.pi + 2 * math.pi * (slot - mid_entrance) / slot_count


def light_theta(light_i):
    return slot_theta(light_to_slot(light_i))


def rank_count():
    """Number of ranks from the entrance up to the far side of the ring."""
    return math.ceil(FRONT_COUNT / 2)


def front_rank(front_i):
    """0 at the entrance edges, rising toward the back of the circle."""
    return min(front_i, FRONT_COUNT - 1 - front_i)


def light_rank(light_i):
    if is_front(light_i):
        return front_rank(light_i)
    return front_rank(front_for_back(light_i))


def pumpkins_at_rank(rank, include_back=True):
    """Light indices at a given rank (both sides of the circle)."""
    result = []
    for i in range(FRONT_COUNT):
        if front_rank(i) == rank:
            result.append(i)
            if include_back:
                outer = back_for(i)
                if outer is not None:
                    result.append(outer)
    return result


def ranks(include_back=True):
    """List of bins: ranks[r] = pumpkins_at_rank(r)."""
    return [pumpkins_at_rank(r, include_back) for r in range(rank_count())]


def rank_bins_ascent(include_back=True):
    """Entrance → back (no return)."""
    return ranks(include_back)


def rank_bins_descent(include_back=True):
    """Back → entrance (no return)."""
    return list(reversed(ranks(include_back)))


def rank_bins_loop(include_back=True):
    """Entrance → back → entrance. Peak rank appears once; lower ranks twice."""
    ascent = ranks(include_back)
    if len(ascent) <= 1:
        return ascent
    return ascent + list(reversed(ascent[:-1]))


def on_color_for(light_i):
    """Cold white on the front ring, warm white on the outer tier."""
    return warm_white if is_back(light_i) else cold_white


def reset_all(lights):
    for light in lights:
        light.set_state(off)


interrupt_pattern_loop = False


class PeriodicLoop:

    def __init__(self, period, length=None):
        self.period = period
        self.next_frame_time = time.perf_counter()
        if length:
            self.finish_time = self.next_frame_time + length
        else:
            self.finish_time = None

    async def next(self):
        self.next_frame_time += self.period
        now = time.perf_counter()
        while now < self.next_frame_time and not interrupt_pattern_loop:
            await asyncio.sleep(0.005)
            now = time.perf_counter()

    def done(self):
        if interrupt_pattern_loop:
            return True
        if self.finish_time:
            return self.next_frame_time >= self.finish_time
        return False


def raw_rgb(r, g, b):
    return {'r': r, 'g': g, 'b': b}


def rgb(r, g, b):
    rgb, cw = rgb2rgbcw((r, g, b))
    red, green, blue = rgb
    state = {'r': r, 'g': g, 'b': b}
    if cw:
        state['c'] = cw
        state['w'] = cw
    return state


def color(c):
    return rgb(round(c.red * 255), round(c.green * 255), round(c.blue * 255))


def dim(c, intensity):
    # return {**{key: value * intensity for (key, value) in c.items()}, 'brightness': intensity}
    return {**c, 'brightness': intensity}


on = {'c': 255, 'w': 255}
off = None

cold_white = {'c': 255}
warm_white = {'w': 255}


@dataclass
class Palette:
    off: ...
    transition: ...
    diverse: ...


the_palettes = [
    Palette(off=raw_rgb(32, 0, 0),
            transition=[
                cold_white, cold_white, warm_white,
                raw_rgb(255, 255, 255),
                raw_rgb(255, 128, 128),
                raw_rgb(255, 0, 0),
                raw_rgb(128, 0, 0)
            ],
            diverse=[
                raw_rgb(255, 32, 32),
                raw_rgb(200, 0, 128),
                raw_rgb(255, 0, 32),
                raw_rgb(255, 0, 0)
            ]),
    Palette(off=raw_rgb(32, 16, 0),
            transition=[
                cold_white, cold_white, warm_white,
                raw_rgb(255, 255, 255),
                raw_rgb(255, 255, 128),
                raw_rgb(255, 255, 0),
                raw_rgb(128, 128, 0)
            ],
            diverse=[
                raw_rgb(255, 32, 0),
                raw_rgb(255, 128, 0),
                raw_rgb(255, 96, 0),
                raw_rgb(192, 64, 0)
            ]),
    Palette(off=raw_rgb(32, 0, 32),
            transition=[
                cold_white, cold_white, warm_white,
                raw_rgb(255, 255, 255),
                raw_rgb(255, 128, 255),
                raw_rgb(255, 0, 255),
                raw_rgb(128, 0, 128)
            ],
            diverse=[
                raw_rgb(255, 0, 128),
                raw_rgb(255, 0, 255),
                raw_rgb(255, 0, 192),
                raw_rgb(192, 0, 64),
                raw_rgb(192, 0, 32)
            ])
]

active_palette = the_palettes[0]


def off_color():
    return active_palette.off


def transition_colors():
    return active_palette.transition


def diverse_palette():
    return active_palette.diverse


def set_active_palette(palette):
    global active_palette
    active_palette = palette
