OSU_RESOLUTION = {"w": 512, "h": 384}


def cs_to_resolution(cs: float):
    """Convert CS value to: resolution, padding and circle_size"""
    r = 54.4 - (4.48 * cs)
    d = 2 * r

    width, w_over = divmod(OSU_RESOLUTION["w"], d)
    padding_x = w_over / (width + 1)

    height, h_over = divmod(OSU_RESOLUTION["h"], d)
    padding_y = h_over / (height + 1)

    return (
        {"w": width, "h": height},
        {"x": padding_x, "y": padding_y},
        {"r": r, "d": d},
    )


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


def ms_to_fps(ms):
    if ms <= 0:
        return 0
    return 1000 / ms
