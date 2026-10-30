import math

import pygame

from utilities import (
    FRONT_COUNT, ENTRANCE_SLOTS, BACK_OF, light_count, slot_count,
    slot_theta, light_to_slot, is_back,
)

# Pumpkin shell tint — visualizer only (physical gourds do this outdoors).
# Colored RGB stays orange-first; dedicated white LEDs (c/w) wash toward bright glow.
PUMPKIN_RGB = (255, 120, 30)
TINT_STRENGTH = 0.88
# Near-white through a lit pumpkin (slight warmth, not pure #fff)
GLOW_WHITE = (255, 248, 235)

BG = (18, 12, 8)
RING_GUIDE = (40, 28, 18)
ENTRANCE_GUIDE = (55, 35, 22)
LABEL = (120, 90, 60)


def state_to_rgb(state):
    if state is None:
        return (0, 0, 0)

    brightness = state.get('brightness', 255) / 255.0

    if 'r' in state or 'g' in state or 'b' in state:
        r = state.get('r', 0)
        g = state.get('g', 0)
        b = state.get('b', 0)
    else:
        c = state.get('c', 0)
        w = state.get('w', 0)
        # Approximate cold / warm white channels as RGB
        r = min(255, w + int(c * 0.85))
        g = min(255, w + int(c * 0.95))
        b = min(255, int(w * 0.85) + c)

    return (int(r * brightness), int(g * brightness), int(b * brightness))


def _lerp_rgb(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def display_color(state):
    """Map a WiZ pilot state to on-screen pumpkin color."""
    if state is None:
        return tuple(int(c * 0.18) for c in PUMPKIN_RGB)

    brightness = state.get('brightness', 255) / 255.0
    r, g, b = state_to_rgb(state)
    if r == g == b == 0:
        return tuple(int(c * 0.18) for c in PUMPKIN_RGB)

    # Orange gel for the color LEDs
    lum = (0.35 * r + 0.55 * g + 0.10 * b) / 255.0
    pr, pg, pb = PUMPKIN_RGB
    t = TINT_STRENGTH
    gelled = (
        int(pr * lum * t + r * (1 - t)),
        int(pg * lum * t + g * (1 - t)),
        int(pb * lum * t + b * (1 - t)),
    )

    # Dedicated white channels punch through the shell toward bright glow
    white_led = max(state.get('c', 0), state.get('w', 0)) / 255.0 * brightness
    peak = max(r, g, b) / 255.0
    floor = min(r, g, b) / 255.0
    rgb_whiteness = (floor / peak if peak > 0 else 0.0) * peak
    wash = min(1.0, white_led * 1.15 + rgb_whiteness * 0.75)

    glow = tuple(int(c * max(lum, white_led)) for c in GLOW_WHITE)
    return _lerp_rgb(gelled, glow, wash)


def _xy(theta, radius, cx, cy):
    return (cx + radius * -math.cos(theta), cy - radius * math.sin(theta))


class CircleRenderer:
    def __init__(self, width=720, height=720):
        pygame.init()
        pygame.display.set_caption("pumpkin-panel visualizer")
        self.screen = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.cx = width / 2
        self.cy = height / 2
        self.front_radius = min(width, height) * 0.32
        self.back_radius = self.front_radius * 1.28
        self.pumpkin_r = max(14, int(min(width, height) * 0.028))
        self.font = pygame.font.SysFont("consolas", 14)

    def light_pos(self, light_i):
        theta = slot_theta(light_to_slot(light_i))
        radius = self.back_radius if is_back(light_i) else self.front_radius
        return _xy(theta, radius, self.cx, self.cy)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
        return True

    def draw(self, lights):
        self.screen.fill(BG)

        pygame.draw.circle(
            self.screen, RING_GUIDE, (int(self.cx), int(self.cy)),
            int(self.front_radius), 1)
        pygame.draw.circle(
            self.screen, RING_GUIDE, (int(self.cx), int(self.cy)),
            int(self.back_radius), 1)

        # Entrance arc guide (virtual slots with no pumpkins)
        if ENTRANCE_SLOTS > 0:
            points = []
            for s in range(FRONT_COUNT, slot_count):
                points.append(_xy(slot_theta(s), self.front_radius, self.cx, self.cy))
            if len(points) >= 2:
                pygame.draw.lines(self.screen, ENTRANCE_GUIDE, False,
                                  [(int(x), int(y)) for x, y in points], 3)

        for i in range(light_count):
            x, y = self.light_pos(i)
            color = display_color(lights[i].get_state())
            pygame.draw.circle(
                self.screen, color, (int(x), int(y)), self.pumpkin_r)
            pygame.draw.circle(
                self.screen, (0, 0, 0), (int(x), int(y)), self.pumpkin_r, 1)

        legend = self.font.render(
            f"N={FRONT_COUNT}  M={ENTRANCE_SLOTS}  backs={BACK_OF}  "
            f"(esc to quit)",
            True, LABEL)
        self.screen.blit(legend, (12, 12))
        pygame.display.flip()

    def close(self):
        pygame.quit()
