#! /usr/bin/env python3

"""
Pyzam
CLI music recognition using python.

"""

import argparse
import asyncio
from pyzam import record
from pyzam import identify
import tempfile

parser = argparse.ArgumentParser(
    prog="Pyzam", description="CLI music recognition using python."
)


def main():
    parser.add_argument(
        "-d", "--duration", help="Audio recording duration (s)", type=int, default=5
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-m",
        "--microphone",
        help="Record from microphone",
        action="store_true",
    )
    group.add_argument(
        "-s",
        "--speaker",
        help="Record from speaker (default)",
        action="store_true",
    )

    args = parser.parse_args()

    temp_dir = tempfile.gettempdir()

    if args.microphone:
        saved_file = record.microphone(
            filename=temp_dir + "/pyzam_audio.wav", seconds=args.duration
        )
    
    if args.speaker:
        saved_file = record.speaker(
            filename=temp_dir + "/pyzam_audio.wav", seconds=args.duration
        )

    asyncio.run(identify.identify_audio(saved_file))


if __name__ == "__main__":
    main()
