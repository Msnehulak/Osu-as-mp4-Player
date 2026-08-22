import subprocess
from pathlib import Path

import numpy as np
from tqdm import tqdm

from OsuBuilder import OsuBuilder

OSU_RESOLUTION = {"w": 512, "h": 384}


class OsuAsMp4Player:
    def __init__(self) -> None:
        pass

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def ms_to_fps(ms):
        if ms <= 0:
            return 0
        return 1000 / ms

    def ffmpeg_decode(self):
        cmd_in = [
            "ffmpeg",
            "-ss",
            str(self.start_sec),
            "-to",
            str(self.end_sec),
            "-i",
            str(self.input_file),
            "-vf",
            f"scale={self.target_size[0]}:{self.target_size[1]},format=gray",
            "-r",
            str(self.target_fps),
            "-f",
            "rawvideo",
            "-pix_fmt",
            "gray",
            "pipe:1",
        ]

        return subprocess.Popen(
            cmd_in, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )

    def extract_audio(self, output_audio_path: Path):
        """Extrahování MP3 audia z videa v určeném časovém rozmezí."""
        cmd = [
            "ffmpeg",
            "-y",
            "-ss",
            str(self.start_sec),
            "-to",
            str(self.end_sec),
            "-i",
            str(self.input_file),
            "-vn",  # Ignorovat video stopu
            "-acodec",
            "libmp3lame",  # Enkódovat do MP3
            "-q:a",
            "2",  # Vysoká kvalita audia (VBR ~190 kbps)
            str(output_audio_path),
        ]
        subprocess.run(
            cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
        )

    def generate(
        self,
        input_file: Path,
        cs: float,
        ar: float,
        od: float,
        use_hd: bool = False,
        start_sec: float = 0.0,
        end_sec: float = 60.0,
    ):
        self.input_file = input_file
        self.start_sec = start_sec
        self.end_sec = end_sec

        res, pad, circle = self.cs_to_resolution(cs)
        self.target_ms = self.arod_to_ms(ar, od, use_hd)
        self.target_fps = self.ms_to_fps(self.target_ms)
        self.target_size = (int(res["w"]), int(res["h"]))

        temp_audio = Path("temp_extracted_audio.mp3")
        print("Extrahuji audio z videa...")
        self.extract_audio(temp_audio)

        osu_map = OsuBuilder(title="test 3", version="Video", cs=cs, ar=ar, od=od)
        osu_map.add_audio(temp_audio)

        process_in = self.ffmpeg_decode()

        offset = 0
        ms_per_frame = self.target_ms
        frame_size = self.target_size[0] * self.target_size[1]

        base_x = pad["x"] + circle["r"]
        base_y = pad["y"] + circle["r"]
        step_x = circle["d"] + pad["x"]
        step_y = circle["d"] + pad["y"]

        expected_frames = int((end_sec - start_sec) * self.target_fps)

        with tqdm(
            total=expected_frames, desc="Processing stream", unit="frame"
        ) as pbar:
            while True:
                raw_frame = process_in.stdout.read(frame_size)
                if not raw_frame or len(raw_frame) < frame_size:
                    break

                frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape(
                    (self.target_size[1], self.target_size[0])
                )

                y_indices, x_indices = np.where(frame <= 127)

                pos_x = (base_x + x_indices * step_x).astype(int)
                pos_y = (base_y + y_indices * step_y).astype(int)

                for x, y in zip(pos_x, pos_y):
                    osu_map.add_circle(x, y, offset)

                offset += ms_per_frame
                pbar.update(1)

        process_in.stdout.close()
        process_in.wait()

        # Uložení mapy (zkopíruje audio.mp3 do tempu a vytvoří .osz)
        osu_map.save("output")

        # Úklid dočasného audio souboru vedle main.py
        if temp_audio.exists():
            temp_audio.unlink()

        print("Hotovo! osu! mapa včetně audia byla vygenerována.")


if __name__ == "__main__":
    app = OsuAsMp4Player()
    app.generate(
        input_file=Path("bad_apple.mp4"),
        cs=6.4,
        ar=10.0,
        od=10.0,
        use_hd=False,
        start_sec=0,
        end_sec=20,
    )
