import pprint

from . import cli, osu_math, video_processor


def main():
    args = cli.main()
    print(f"args: {args}")
    vals = {
        **osu_math.cs_to_resolution(args.cs),
        "offset": osu_math.arod_to_ms(ar=args.ar, od=args.od),
    }

    video_processor.main(vals, args)

    pprint.pprint(vals)
