from . import cli, osu_math


def main():
    args = cli.main()
    print(f"args: {args}")
    print(osu_math.ms_to_fps(osu_math.arod_to_ms(-35, 0)))
