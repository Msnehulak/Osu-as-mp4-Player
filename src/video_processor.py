import subprocess
import time

import numpy as np

from . import map_generator

THRESHOLD = 128


def ms_to_fps(ms):
    if ms <= 0:
        return 0
    return 1000 / ms


def main(vals, args):
    mg = map_generator.MapGenerator()

    width = vals["resolution"]["w"]
    height = vals["resolution"]["h"]
    fps = ms_to_fps(vals["offset"])

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(args.file),
        "-vf",
        f"scale={width}:{height},fps={fps},format=gray",
        "-pix_fmt",
        "gray",
        "-f",
        "rawvideo",
        "-",
    ]

    frame_bytes = width * height  # gray = 1 kanál

    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        while True:
            raw = proc.stdout.read(frame_bytes)
            if len(raw) < frame_bytes:
                break

            frame = np.frombuffer(raw, np.uint8).reshape(height, width)

            # 1 = světlý pixel (bílý), 0 = tmavý (černý)
            binary = (frame > THRESHOLD).astype(np.uint8)

            mg.process_frame(frame)

            break
