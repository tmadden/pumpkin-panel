"""Run with:  python -m visualizer

Optional pattern key:  python -m visualizer t
  s=snake  t=twinkle  f=fairies  a=rotator  p=progression
"""

import asyncio
import sys

import utilities
from utilities import light_count
from show import control_loop, pattern_keys
import show
from visualizer.mock_light import MockLight
from visualizer.render import CircleRenderer


async def draw_loop(renderer, lights):
    while renderer.handle_events():
        renderer.draw(lights)
        await asyncio.sleep(1 / 30)


async def main():
    if len(sys.argv) > 1:
        key = sys.argv[1]
        if key in pattern_keys:
            show.current_pattern = pattern_keys[key]
            print(f"Pattern: {key} ({show.current_pattern.__name__})", flush=True)
        else:
            print(f"Unknown pattern key {key!r}. Options: {sorted(pattern_keys)}",
                  flush=True)
            return
    else:
        print("Pattern: rotator (pass s/t/f/a/p to pick one)", flush=True)

    print("Visualizer — layout from utilities.py (esc / close window to quit)",
          flush=True)

    lights = [MockLight() for _ in range(light_count)]
    renderer = CircleRenderer()

    show_task = asyncio.create_task(control_loop(lights))
    draw_task = asyncio.create_task(draw_loop(renderer, lights))

    try:
        await draw_task
    finally:
        utilities.interrupt_pattern_loop = True
        show_task.cancel()
        try:
            await show_task
        except asyncio.CancelledError:
            pass
        renderer.close()


if __name__ == "__main__":
    asyncio.run(main())
