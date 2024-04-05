import asyncio
import csv
from datetime import datetime
import random
from rich.progress import MofNCompleteColumn, Progress, TimeElapsedColumn
from shazamio import Shazam
import soundfile as sf
import tempfile
import time
import os


def write_csv(file_name: str, data_rows: list):
    """
    Writes the found song's data into a CSV file.

    :param file_name: Name for csv file
    :param data_rows: Includes timestamp, track_title, artist and album_cover.
    """
    header = ["Timestamp", "Track", "Artist", "Album Cover"]
    csv_file = f"{file_name}.csv"
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(data_rows)


def extract_track_info(out):
    track_title = out["track"]["title"]
    artist = out["track"]["subtitle"]
    if "images" in out["track"]:
        album_cover_hq = (
            out["track"]
            .get("images", {})
            .get("coverart", "")
            .replace("/400x400cc.jpg", "/1400x1400cc.png")
        )
    else:
        album_cover_hq = None
    return track_title, artist, album_cover_hq


def print_track_info(track_info):
    print(f"Track: {track_info[0]}")
    print(f"Artist: {track_info[1]}")
    print(f"Album Cover: {track_info[2]}")


async def identify_audio(
    audio_file: str, json=False, write=False, timestamp=None, file_name=None
):
    """
    Identifies the song of a given audio file.

    file_name is set to "{audio_file}" if none is provided.

    :param audio_file: Path to audio file.
    :param json: If true, function returns the whole shazamio output as JSON.
    :param write: If true, output is written in CSV file. Timestamp is required if write is True.
    :param timestamp: Time at which the song was recognized. Required for write.
    :param file_name (Optional): Name for csv file Only used if write is True.
    """
    if not os.path.exists(audio_file):
        print(f"Error: File '{audio_file}' not found.")
        return
    # Shazam's maximum API call limit is 20 requests per minute.
    # To avoid API call limits, Shazamio needs to a proxy.
    shazam = Shazam()
    out = await shazam.recognize(data=audio_file, proxy=None)

    if "track" not in out:
        print("No matches found.")
        return

    if json:
        print(out)
        return

    track_info = extract_track_info(out)
    print_track_info(track_info)

    if write:
        file_name = file_name or os.path.splitext(os.path.basename(audio_file))[0]
        write_csv(file_name, [timestamp, *track_info])


def split_and_identify(audio_file: str, duration: int):
    """
    Splits audio file by duration (seconds) and identifies songs. Writes the csv file automatically.

    :param audio_file: Path to audio file.
    :param duration: Length of each segment (seconds).
    """
    if not os.path.exists(audio_file):
        print(f"Error: File '{audio_file}' not found.")
        return

    file_name = os.path.splitext(os.path.basename(audio_file))[0]
    print(f"Reading {audio_file}...")
    data, samplerate = sf.read(audio_file)
    samples_per_duration = samplerate * duration
    num_segments = len(data) // samples_per_duration

    with Progress(
        TimeElapsedColumn(),
        MofNCompleteColumn(),
        *Progress.get_default_columns(),
    ) as progress:
        task = progress.add_task(
            f"[green]Splitting and identifying audio...", total=num_segments
        )
        # Make each segment an audio file to be used in Shazamio.
        for i in range(num_segments):
            start_idx = i * samples_per_duration
            segment_data = data[start_idx : start_idx + samples_per_duration]
            timestamp = datetime.utcfromtimestamp(start_idx / samplerate).strftime(
                "%H:%M:%S"
            )
            # Temporarily saves audio file, shazams, then deletes.
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                sf.write(temp_file.name, segment_data, samplerate)
                asyncio.run(
                    identify_audio(
                        temp_file.name,
                        json=False,
                        write=True,
                        timestamp=timestamp,
                        file_name=f"mixtape_{file_name}_{duration}sec",
                    )
                )
                temp_file.close()
                os.remove(temp_file.name)
            progress.update(task, advance=1)
            time.sleep(2)  # Throttle requests to < 20/minute or Error 429.
