#! /usr/bin/env python3

"""
Pyzam
CLI music recognition using python.

"""

import argparse
import asyncio
import record
from identify import identify_audio
import tempfile

parser = argparse.ArgumentParser(
    prog="Pyzam", description="CLI music recognition using python."
)


def main():
    parser.add_argument(
        "-d", "--duration", help="Audio recording duration (s)", type=int, default=5
    )

    args = parser.parse_args()

    temp_dir = tempfile.gettempdir()

    saved_file = record.speaker(
        filename=temp_dir + "/pyzam_audio.wav", seconds=args.duration
    )

    asyncio.run(identify_audio(saved_file))


if __name__ == "__main__":
    main()
