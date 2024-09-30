#! /usr/bin/env python3

"""
Pyzam 0.12.3
A CLI music recognition tool for audio and mixtapes.
"""

import argparse
import asyncio
from datetime import datetime
from pathlib import Path
from pyzam import identify, record
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
    run_group = parser.add_mutually_exclusive_group()
    output_group = parser.add_mutually_exclusive_group()

    input_group.add_argument(
        "--input", type=Path, help="detect from the given audio input file"
    )
    input_group.add_argument(
        "-m", "--microphone", action="store_true", help="record audio from microphone"
    )
    input_group.add_argument(
        "-s",
        "--speaker",
        action="store_true",
        help="record audio from speaker (default)",
    )
    input_group.add_argument(
        "-u",
        "--url",
        help="Detect from an audio URL",
    )

    parser.add_argument(
        "-d", "--duration", type=int, default=5, help="audio recording duration (s)"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="suppress operation messages"
    )
    run_group.add_argument(
        "--loop", "-l", action="store_true", help="loop music recognition process"
    )
    run_group.add_argument(
        "--mixtape", action="store_true", help="Identifies songs of a mixtape"
    )
    output_group.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="emits the whole shazamio response as raw JSON",
    )
    output_group.add_argument(
        "-w", "--write", action="store_true", help="writes the output as a file"
    )

    return parser


def check_ffmpeg():
    if not shutil.which("ffmpeg"):
        print("[red]Fatal: ffmpeg not found on $PATH[/red]")
        sys.exit(1)


def get_input_file(args, temp_dir) -> Path:
    if args.microphone:
        return record.microphone(
            filename=f"{temp_dir}/pyzam_mic.wav", seconds=args.duration, quiet=args.quiet
        )
    elif args.speaker:
        return record.speaker(
            filename=f"{temp_dir}/pyzam_speaker.wav", seconds=args.duration, quiet=args.quiet
        )
    elif args.url:
        return record.url(
            url=args.url, filename=f"{temp_dir}/pyzam_url.wav", quiet=args.quiet
        )
    else:
        return args.input


def process_mixtape(input_file, duration):
    song = sf.SoundFile(str(input_file))
    audio_length = song.frames / song.samplerate
    iterations = int(-(-audio_length // duration))
    print(f"Get ready, we are Pyzaming {iterations} times...")
    identify.split_and_identify(str(input_file), duration)


def identify_audio(input_file, args):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    asyncio.run(
        identify.identify_audio(
            str(input_file), json=args.json, write=args.write, timestamp=current_time
        )
    )


def main() -> None:
    check_ffmpeg()
    parser = _parser()
    args = parser.parse_args()

    # Check if  --input or --url and --loop are used together
    if args.input and args.loop:
        parser.error("--loop is only allowed with --microphone or --speaker")
    if args.url and args.loop:
        parser.error("--loop is only allowed with --microphone or --speaker")

    # Check if --mixtape and (--microphone or --speaker) are used together
    if args.mixtape and (args.microphone or args.speaker):
        parser.error("--mixtape is only allowed with --input or --url")

    temp_dir = tempfile.gettempdir()

    while True:
        input_file = get_input_file(args, temp_dir)
        if args.mixtape:
            process_mixtape(input_file, args.duration)
            break
        identify_audio(input_file, args)
        if not args.loop:
            break


if __name__ == "__main__":
    main()
