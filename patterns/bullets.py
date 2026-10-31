import random
from dataclasses import dataclass

from utilities import *


@dataclass
class Bullet:
    pos: int
    direction: int  # +1 from right gate, -1 from left gate
    color: ...


@dataclass
class Flash:
    positions: tuple
    step: int = 0


@dataclass
class Gate:
    front: int
    direction: int
    flash_ticks: int = 0
    cooldown: int = 0


def _left():
    return front_count - 1


def _right():
    return 0


def _entrance_lights(front):
    out = [front]
    outer = back_for(front)
    if outer is not None:
        out.append(outer)
    return out


def _steps_to_far_gate(pos, direction):
    target = _left() if direction == 1 else _right()
    cur = pos
    for steps in range(1, front_count + 1):
        cur = step_front(cur, direction)
        if cur == target:
            return steps
    return front_count


async def bullets(lights, time_limit, auto_intercept=True, intercept_range=3):
    """Gates glow warm white and fire diverse bullets along the front arc.

    Each gate fires on its own random schedule. With auto_intercept, a gate
    that has no bullet in flight will fire when an enemy bullet comes within
    intercept_range pumpkins. Otherwise bullets that reach the far gate vanish.
    """
    for light in lights:
        light.set_state(off)

    gates = [
        Gate(front=_right(), direction=1, cooldown=random.randint(3, 8)),
        Gate(front=_left(), direction=-1, cooldown=random.randint(8, 16)),
    ]
    live = []
    flashes = []

    def fire(gate):
        gate.flash_ticks = 3
        live.append(Bullet(
            pos=step_front(gate.front, gate.direction),
            direction=gate.direction,
            color=random.choice(diverse_palette()),
        ))
        gate.cooldown = random.randint(10, 20)

    def has_flight(direction):
        return any(b.direction == direction for b in live)

    loop = PeriodicLoop(0.11, time_limit)
    while not loop.done():
        for g in gates:
            if g.flash_ticks > 0:
                g.flash_ticks -= 1
            if g.cooldown > 0:
                g.cooldown -= 1
            elif random.random() < 0.1:
                fire(g)

        if auto_intercept:
            for g in gates:
                if has_flight(g.direction):
                    continue
                threat = any(
                    b.direction == -g.direction
                    and _steps_to_far_gate(b.pos, b.direction) <= intercept_range
                    for b in live)
                if threat:
                    fire(g)

        old_pos = {id(b): b.pos for b in live}
        for b in live:
            b.pos = step_front(b.pos, b.direction)

        live = [
            b for b in live
            if b.pos != (_left() if b.direction == 1 else _right())
        ]

        dead = set()
        by_pos = {}
        for b in live:
            by_pos.setdefault(b.pos, []).append(b)

        for pos, group in by_pos.items():
            if len(group) >= 2:
                for b in group:
                    dead.add(id(b))
                flashes.append(Flash(positions=(pos,), step=0))

        remaining = [b for b in live if id(b) not in dead]
        for i, a in enumerate(remaining):
            for b in remaining[i + 1:]:
                if id(a) in dead or id(b) in dead:
                    continue
                if a.direction != -b.direction:
                    continue
                if (a.pos == old_pos.get(id(b))
                        and b.pos == old_pos.get(id(a))):
                    dead.add(id(a))
                    dead.add(id(b))
                    flashes.append(Flash(positions=(a.pos, b.pos), step=0))

        live = [b for b in remaining if id(b) not in dead]

        colors = transition_colors()
        next_flashes = []
        for fl in flashes:
            fl.step += 1
            if fl.step <= len(colors) + 1:
                next_flashes.append(fl)
        flashes = next_flashes

        for i in range(light_count):
            lights[i].set_state(off)

        for b in live:
            lights[b.pos].set_state(b.color, seriously=True)

        for fl in flashes:
            if fl.step <= 1:
                color = cold_white
            else:
                color = colors[min(fl.step - 2, len(colors) - 1)]
            for pos in fl.positions:
                lights[pos].set_state(color, seriously=(fl.step <= 1))

        flash_cells = {p for fl in flashes for p in fl.positions}
        bullet_cells = {b.pos for b in live}
        for g in gates:
            color = cold_white if g.flash_ticks > 0 else warm_white
            for i in _entrance_lights(g.front):
                if i in bullet_cells or i in flash_cells:
                    continue
                lights[i].set_state(color, seriously=(g.flash_ticks > 0))

        await loop.next()
