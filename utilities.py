import asyncio
import math
import time

def index(p):
    return p[0] * 4 + p[1]

def in_bounds(p):
    return p[0] >= 0 and p[0] < 4 and p[1] >= 0 and p[1] < 4

def flipped(v):
    return [-v[0], -v[1]]

def equal(a, b):
    return round(a[0]) == round(b[0]) and round(a[1]) == round(b[1])

def reset_all(lights):
    for light in lights:
        light.set_state(off)


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
        await asyncio.sleep(self.next_frame_time - now)

    def done(self):
        if self.finish_time:
            return self.next_frame_time >= self.finish_time
        return False

def rgb(r, g, b):
    return {'r': r, 'g': g, 'b': b}

def color(c):
    return {'r': round(c.red * 255), 'g': round(c.green * 255), 'b': round(c.blue * 255)}

on = {'c': 255, 'w': 255}
off = None
