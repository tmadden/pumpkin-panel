import random
from dataclasses import dataclass

from utilities import *


@dataclass
class Fairy:
    pos: int
    mode: str  # 'dart' | 'hover'
    dart_delta: int
    dart_left: int
    hover_ticks: int
    hover_phase: int
    hover_partner: ...
    hover_style: str  # 'solo' | 'ab' | 'echo'


def _pick_dart(pos):
    return random.choice([-1, 1]), random.randint(2, 3)


def _start_hover(fairy):
    fairy.mode = 'hover'
    fairy.hover_ticks = random.randint(8, 16)
    fairy.hover_phase = 0
    styles = ['solo', 'ab']
    if is_front(fairy.pos) and back_for(fairy.pos) is not None:
        styles.append('echo')
    fairy.hover_style = random.choice(styles)
    if fairy.hover_style == 'ab':
        base = fairy.pos if is_front(fairy.pos) else front_for_back(fairy.pos)
        fairy.hover_partner = step_front(base, random.choice([-1, 1]))
    elif fairy.hover_style == 'echo':
        fairy.hover_partner = back_for(fairy.pos)
    else:
        fairy.hover_partner = None


def _off(lights, i, background):
    lights[i].set_state(background)


def _on(lights, i, seriously=False):
    lights[i].set_state(on_color_for(i), seriously=seriously)


async def fairies(lights, time_limit):
    background = off_color()
    for light in lights:
        light.set_state(background)

    starts = [0, front_count // 3, (2 * front_count) // 3]
    fairies_ = []
    for i, start in enumerate(starts):
        f = Fairy(
            pos=start,
            mode='dart',
            dart_delta=1 if i % 2 == 0 else -1,
            dart_left=random.randint(2, 3),
            hover_ticks=0,
            hover_phase=0,
            hover_partner=None,
            hover_style='solo',
        )
        if i > 0:
            _start_hover(f)
            f.hover_ticks = i * 4
        fairies_.append(f)
        _on(lights, f.pos, seriously=True)

    loop = PeriodicLoop(0.07, time_limit)
    while not loop.done():
        background = off_color()
        for f in fairies_:
            if f.mode == 'dart':
                _off(lights, f.pos, background)
                if is_back(f.pos):
                    f.pos = front_for_back(f.pos)
                f.pos = step_front(f.pos, f.dart_delta)
                if (is_front(f.pos) and back_for(f.pos) is not None
                        and f.dart_left == 1 and random.random() < 0.35):
                    f.pos = back_for(f.pos)
                _on(lights, f.pos, seriously=True)
                f.dart_left -= 1
                if f.dart_left <= 0:
                    _start_hover(f)
            else:
                f.hover_phase += 1
                f.hover_ticks -= 1
                bright = f.hover_phase % 4 < 2

                if f.hover_style == 'solo':
                    if bright:
                        _on(lights, f.pos)
                    else:
                        _off(lights, f.pos, background)
                elif f.hover_style == 'ab' and f.hover_partner is not None:
                    if bright:
                        _off(lights, f.hover_partner, background)
                        _on(lights, f.pos)
                    else:
                        _off(lights, f.pos, background)
                        _on(lights, f.hover_partner)
                elif f.hover_style == 'echo' and f.hover_partner is not None:
                    if bright:
                        _on(lights, f.pos, seriously=True)
                        _off(lights, f.hover_partner, background)
                    else:
                        _off(lights, f.pos, background)
                        _on(lights, f.hover_partner, seriously=True)

                if f.hover_ticks <= 0:
                    if f.hover_partner is not None:
                        _off(lights, f.hover_partner, background)
                    _on(lights, f.pos, seriously=True)
                    f.dart_delta, f.dart_left = _pick_dart(f.pos)
                    f.mode = 'dart'

        await loop.next()
