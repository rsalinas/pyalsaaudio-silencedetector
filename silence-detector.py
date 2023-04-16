#!/usr/bin/env python3
# Written by Raúl Salinas-Monteagudo 2023-04-07

import alsaaudio
import argparse
import numpy as np
import os
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument(
    "--threshold", type=int, default=500, help="set threshold (defaults to 500)"
)
parser.add_argument(
    "--length",
    type=float,
    default=2,
    help="seconds of silence to detect (defaults to 2 seconds)",
)
parser.add_argument(
    "--on-silence",
    default="./on-silence.sh",
    help="code to run on silence",
)
parser.add_argument(
    "--on-sound", default="./on-sound.sh", help="code to run on sound"
)
parser.add_argument("--monitor", action="store_true", help="run volume monitor")


def main():
    args = parser.parse_args()
    device = alsaaudio.PCM(
        alsaaudio.PCM_CAPTURE,
        alsaaudio.PCM_NORMAL,
        channels=1,
        rate=44100,
        periodsize=int(44100 / 10) if args.monitor else int(44100 / 1000),
        format=alsaaudio.PCM_FORMAT_S16_LE,
    )

    silent_time = 0
    silent = False
    print("Starting detection...", file=sys.stderr, flush=True)
    while True:
        length, data = device.read()
        if not length:
            return 1

        samples = np.frombuffer(data, dtype=np.int16)
        volume = max(abs(sample) for sample in samples)
        if args.monitor:
            print(volume)
            continue
        if volume > args.threshold:
            silent_time = 0
            if silent:
                os.system(args.on_sound)
                silent = False
                silent_time = 0
        else:
            silent_time += 1
        if not silent and silent_time > args.length * 44100 / length:
            silent = True
            os.system(args.on_silence)


if __name__ == "__main__":
    sys.exit(main())
