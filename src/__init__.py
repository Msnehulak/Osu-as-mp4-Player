from . import argparser, osu_math

args = argparser.main()
print(f"args: {args}")
print(osu_math.ms_to_fps(osu_math.arod_to_ms(-35, 0)))
