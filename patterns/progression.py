from utilities import PeriodicLoop, off_color, on_color_for


def _bin_at(bins, index):
    if index < 0 or index >= len(bins):
        return []
    return bins[index]


async def progression(lights,
                      bins,
                      time_limit=None,
                      on_count=6,
                      window=None,
                      period=0.1,
                      loop=False,
                      on_fn=None,
                      off_fn=None):
    """Sweep an ordered list of bins with a sliding trail of lit pumpkins.

    `on_count` is how many pumpkins stay lit in the wipe (packaged with each
    transition ordering). `window` is accepted as an alias for older callers.
    """
    if window is not None:
        on_count = window
    if on_fn is None:
        on_fn = on_color_for
    if off_fn is None:
        off_fn = lambda _i: off_color()

    n = len(bins)
    if n == 0 or on_count <= 0:
        return

    loop_timer = PeriodicLoop(period, time_limit)
    step = 0
    trail = []  # ordered pumpkin indices currently in the white wipe
    max_steps = None if loop else n + on_count

    while not loop_timer.done():
        if max_steps is not None and step >= max_steps:
            break

        if loop:
            on_bin = bins[step % n] if n else []
        else:
            on_bin = _bin_at(bins, step)

        prev_on = set(trail)
        for i in on_bin:
            if i in trail:
                trail.remove(i)
            trail.append(i)
        while len(trail) > on_count:
            trail.pop(0)

        now_on = set(trail)
        for i in prev_on - now_on:
            lights[i].set_state(off_fn(i))
        for i in on_bin:
            if i in now_on:
                lights[i].set_state(on_fn(i), seriously=True)
        # Re-assert trail (in case of overlap with off_fn)
        for i in now_on:
            if i not in on_bin:
                lights[i].set_state(on_fn(i))

        step += 1
        await loop_timer.next()

    # Clear any remaining trail when not looping forever
    if not loop:
        for i in trail:
            lights[i].set_state(off_fn(i))
