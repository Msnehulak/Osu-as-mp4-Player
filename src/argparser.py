import argparse
import sys
from pathlib import Path

DEFAULT_VALUERS = {}


def main():
    parser = argparse.ArgumentParser(description="Osu as mp4 player")
    parser.add_argument(
        "-ar", "--ApproachRate", help="AR setup", dest="ar", type=float, default=5
    )
    parser.add_argument(
        "-cs", "--CircleSize", help="CS setup", dest="cs", type=float, default=5
    )
    parser.add_argument(
        "-hp", "--HPDrainRate", help="AR setup", dest="hp", type=float, default=5
    )
    parser.add_argument(
        "-od", "--OverallDifficulty", help="CS setup", type=float, dest="od", default=5
    )
    parser.add_argument("-f", "--file", help="Input file", type=Path, default=None)
    args = parser.parse_args()

    if args.file is None:
        import tkinter as tk

        from native_file_dialog import tkinter as dialogs

        root = tk.Tk()
        root.withdraw()

        paths = dialogs.open_file(
            master=root, filters=[("Videa", "*.mp4 *.mkv *.avi *.mov *.webm")]
        )

        if paths:
            if len(paths) > 1:
                sys.exit("ERROR: Pleas select 1 vido file!!")
            args.file = Path(paths[0])
        else:
            sys.exit("ERROR: Pleas select vido file!!")

    return args
