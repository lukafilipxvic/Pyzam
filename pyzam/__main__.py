#! /usr/bin/env python3

"""
Pyzam
CLI music recognition in python.

"""

import argparse
import asyncio
from pathlib import Path
from pyzam import record
from pyzam import identify
import shutil
import sys
import tempfile
import time


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="Pyzam",
        description="CLI music recognition in python.",
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "-m", "--microphone", help="record from microphone", action="store_true"
    )
    input_group.add_argument(
        "-s", "--speaker", help="record from speaker (default)", action="store_true"
    )
    input_group.add_argument(
        "--input", type=Path, help="detect from the given audio input file"
    )

    parser.add_argument(
        "-d", "--duration", help="Audio recording duration (s)", type=int, default=5
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="emit Shazam's response as JSON on stdout",
    )
    return parser


def main() -> None:
    parser = _parser()
    args = parser.parse_args()

    if not shutil.which("ffmpeg"):
        print("[red]Fatal: ffmpeg not found on $PATH[/red]")
        sys.exit(1)

    temp_dir = tempfile.gettempdir()

    if args.microphone:
        saved_file = record.microphone(
            filename=temp_dir + "/pyzam_audio.wav", seconds=args.duration
        )
    if args.speaker:
        saved_file = record.speaker(
            filename=temp_dir + "/pyzam_audio.wav", seconds=args.duration
        )
    if args.input:  # Input is path to file
        saved_file = args.input

    asyncio.run(identify.identify_audio(saved_file, json=args.json))


if __name__ == "__main__":
    main()
