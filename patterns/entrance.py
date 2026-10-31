import random
import time
from dataclasses import dataclass, field

from utilities import *


def _with_backs(fronts):
    out = []
    for f in fronts:
        out.append(f)
        outer = back_for(f)
        if outer is not None:
            out.append(outer)
    return out


def _expired(deadline):
    return interrupt_pattern_loop or (
        deadline is not None and time.perf_counter() >= deadline)


@dataclass
class Spirit:
    rank: int
    phase: str  # enter_pulse | march | settle_pulse | fade
    tick: int = 0
    pos_r: int = 0
    pos_l: int = 0
    target_r: int = 0
    target_l: int = 0
    fade_colors: list = field(default_factory=list)
    settle_color: ... = None


# Timing (main loop period ≈ 0.2s)
ENTER_PULSE = 5
SETTLE_PULSE = 5
SPAWN_EVERY = 12  # new spirit while others still walking/settling
MARCH_EVERY = 3  # steps only every N ticks → slower walk
HOLD_FULL = 10


def _spirit_lights(spirit):
    if spirit.phase in ('enter_pulse',):
        fronts = [0, front_count - 1]
    elif spirit.phase == 'march':
        fronts = [spirit.pos_r, spirit.pos_l]
    else:
        fronts = [spirit.target_r, spirit.target_l]
    return _with_backs(fronts)


def _spirit_color(spirit):
    if spirit.phase in ('enter_pulse', 'settle_pulse'):
        return cold_white if spirit.tick % 2 == 0 else warm_white
    if spirit.phase == 'march':
        return None  # use on_color_for per light
    if spirit.phase == 'fade':
        idx = min(spirit.tick, len(spirit.fade_colors) - 1)
        return spirit.fade_colors[idx]
    return cold_white


def _advance(spirit):
    """Advance one tick. Return True if the spirit has settled into full_colors."""
    spirit.tick += 1

    if spirit.phase == 'enter_pulse':
        if spirit.tick >= ENTER_PULSE:
            spirit.phase = 'march'
            spirit.tick = 0
            spirit.pos_r = 0
            spirit.pos_l = front_count - 1
            # Already at target (e.g. last entrance rank)? skip march
            if spirit.pos_r == spirit.target_r and spirit.pos_l == spirit.target_l:
                spirit.phase = 'settle_pulse'
                spirit.tick = 0

    elif spirit.phase == 'march':
        if spirit.tick % MARCH_EVERY == 0:
            if spirit.pos_r != spirit.target_r:
                spirit.pos_r = step_front(spirit.pos_r, 1)
            if spirit.pos_l != spirit.target_l:
                spirit.pos_l = step_front(spirit.pos_l, -1)
        if spirit.pos_r == spirit.target_r and spirit.pos_l == spirit.target_l:
            spirit.phase = 'settle_pulse'
            spirit.tick = 0

    elif spirit.phase == 'settle_pulse':
        if spirit.tick >= SETTLE_PULSE:
            spirit.phase = 'fade'
            spirit.tick = 0
            spirit.fade_colors = list(transition_colors())
            spirit.settle_color = random.choice(diverse_palette())

    elif spirit.phase == 'fade':
        if spirit.tick >= len(spirit.fade_colors):
            return True

    return False


async def entrance(lights, time_limit):
    """Spirits enter on a cadence, walk slowly to ranks (back→front), settle diverse."""
    for light in lights:
        light.set_state(off)

    deadline = (time.perf_counter() + time_limit) if time_limit else None
    full_colors = {}
    spirits = []
    n_ranks = rank_count()
    next_rank = n_ranks - 1
    spawn_cooldown = 0
    hold_ticks = 0

    loop = PeriodicLoop(0.2, time_limit)
    while not _expired(deadline) and not loop.done():
        # Spawn next spirit on a regular interval
        if spawn_cooldown > 0:
            spawn_cooldown -= 1
        elif next_rank >= 0:
            spirits.append(Spirit(
                rank=next_rank,
                phase='enter_pulse',
                tick=0,
                target_r=next_rank,
                target_l=front_count - 1 - next_rank,
            ))
            next_rank -= 1
            spawn_cooldown = SPAWN_EVERY

        # Advance spirits; fold finished into full_colors
        still = []
        for sp in spirits:
            done = _advance(sp)
            if done:
                for i in _with_backs([sp.target_r, sp.target_l]):
                    full_colors[i] = sp.settle_color
            else:
                still.append(sp)
        spirits = still

        # All ranks full and quiet → brief hold, then clear for another pass
        if next_rank < 0 and not spirits:
            hold_ticks += 1
            if hold_ticks >= HOLD_FULL:
                full_colors.clear()
                next_rank = n_ranks - 1
                spawn_cooldown = 0
                hold_ticks = 0
                for light in lights:
                    light.set_state(off)
        else:
            hold_ticks = 0

        # Paint: full ranks + active spirits; everything else fully off
        active = {}
        for sp in spirits:
            color = _spirit_color(sp)
            for i in _spirit_lights(sp):
                if color is None:
                    active[i] = on_color_for(i)
                else:
                    active[i] = color

        for i in range(light_count):
            if i in full_colors and i not in active:
                lights[i].set_state(full_colors[i])
            elif i in active:
                lights[i].set_state(active[i], seriously=True)
            else:
                lights[i].set_state(off)

        await loop.next()
