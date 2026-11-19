import subprocess

import numpy as np

INPUT = "input.mp4"
W, H = 640, 360
FPS = 10
CHANNELS = 3
PIX_FMT = "rgb24" if CHANNELS == 3 else "gray"

cmd = [
    "ffmpeg",
    "-hide_banner",
    "-loglevel",
    "error",
    "-i",
    INPUT,
    "-vf",
    f"scale={W}:{H},fps={FPS}",
    "-pix_fmt",
    PIX_FMT,
    "-f",
    "rawvideo",
    "-",
]

frame_bytes = W * H * CHANNELS

with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
    idx = 0
    while True:
        raw = proc.stdout.read(frame_bytes)
        if len(raw) < frame_bytes:
            break
        frame = np.frombuffer(raw, np.uint8).reshape(H, W, CHANNELS)

        # --- tady máš přístup k pixelům ---
        # frame[y, x]      -> pixel
        # frame[:, :, 0]   -> R kanál (u rgb24)
        # frame.mean()     -> průměr
        print(idx, frame.shape, frame.dtype, frame[0, 0])
        idx += 1
