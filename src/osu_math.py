import sys
from typing import NamedTuple

OSU_RESOLUTION = {"w": 512, "h": 384}


def cs_to_resolution(cs: float):
    """Convert CS value to: resolution, padding and circle_size."""
    radius = 54.4 - (4.48 * cs)
    diameter = 2 * radius

    if diameter <= 0:
        raise ValueError(
            f"CS={cs} produces a non-positive circle diameter ({diameter:.2f}). "
            f"CS must be < {54.4 / 4.48:.2f}."
        )

    width = int(OSU_RESOLUTION["w"] // diameter)
    height = int(OSU_RESOLUTION["h"] // diameter)

    if width < 1 or height < 1:
        min_cs = (108.8 - OSU_RESOLUTION["h"]) / 8.96
        raise ValueError(
            f"CS={cs} gives circles too large for the "
            f"{OSU_RESOLUTION['w']}x{OSU_RESOLUTION['h']} playfield "
            f"(diameter={diameter:.2f}, grid={width}x{height}). "
            f"Minimum supported CS is {min_cs:.2f}."
        )

    padding_x = (OSU_RESOLUTION["w"] - width * diameter) / (width + 1)
    padding_y = (OSU_RESOLUTION["h"] - height * diameter) / (height + 1)

    return {
        "resolution": {"w": width, "h": height},
        "padding": {"x": padding_x, "y": padding_y},
        "circle_size": {"r": radius, "d": diameter},
    }


def arod_to_ms(ar: float, od: float, use_hd: bool = False):
    if ar < 5:
        t = 1200 + 120 * (5 - ar)
    elif ar == 5:
        t = 1200
    else:
        t = 1200 - 150 * (ar - 5)

    if use_hd:
        return t * 0.7

    w50 = 200 - 10 * od

    return t + w50
