#! /usr/bin/env python3

"""
Pyzam
CLI music recognition in python.

"""

import argparse
import asyncio
from datetime import datetime
from pathlib import Path
from pyzam import identify
from pyzam import record
import shutil
import soundfile as sf
import sys
import tempfile


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="Pyzam",
        description="CLI music recognition in python.",
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "-m", "--microphone", help="record audio from microphone", action="store_true"
    )
    input_group.add_argument(
        "-s",
        "--speaker",
        help="record audio from speaker (default)",
        action="store_true",
    )
    input_group.add_argument(
        "--input", type=Path, help="detect from the given audio input file"
    )

    parser.add_argument(
        "-d", "--duration", help="audio recording duration (s)", type=int, default=5
    )
    parser.add_argument(
        "-l", "--loop", help="loop music recognition process", action="store_true"
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="emits the whole shazamio response as raw JSON",
    )
    parser.add_argument(
        "-w", "--write", help="writes the output as a file", action="store_true"
    )
    parser.add_argument(
        "--mixtape", help="Identifies songs of a mixtape", action="store_true"
    )
    return parser


def main() -> None:
    parser = _parser()
    args = parser.parse_args()

    if not shutil.which("ffmpeg"):
        print("[red]Fatal: ffmpeg not found on $PATH[/red]")
        sys.exit(1)

    temp_dir = tempfile.gettempdir()

    while True:
        if args.microphone:
            input = record.microphone(
                filename=temp_dir + "/pyzam_mic.wav", seconds=args.duration
            )
        if args.speaker:
            input = record.speaker(
                filename=temp_dir + "/pyzam_speaker.wav", seconds=args.duration
            )
        if args.input:
            input = args.input
            if args.mixtape:
                song = sf.SoundFile(input.__str__())
                audio_length = song.frames / song.samplerate
                iterations = int(-(-audio_length // args.duration))
                print(f"Get ready, we are Pyzaming {iterations} times...")
                identify.split_and_identify(input.__str__(), args.duration)
                break

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        asyncio.run(
            identify.identify_audio(
                input.__str__(),
                json=args.json,
                write=args.write,
                timestamp=current_time,
            )
        )

        if not args.loop:
            break


if __name__ == "__main__":
    main()
