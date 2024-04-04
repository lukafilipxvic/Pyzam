import asyncio
import csv
from datetime import datetime
import random
from rich.progress import Progress
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
    file_exists = os.path.isfile(f"{file_name}.csv")

    with open(f"{file_name}.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(data_rows)


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
    :param file_name (Optional): Name for csv file Only valid if write True.
    """
    if not os.path.exists(audio_file):
        print(f"Error: File '{audio_file}' not found.")
        return
    # Shazam's maximum API call limit is 20 requests per minute.
    # To avoid API call limits, Shazamio's http_client needs to a proxy.
    # We can make the requests with proxies.
    # 20% ≈ 1 change for 5 calls
    shazam = Shazam(endpoint_country=random.choices(['AU', 'US'], weights=[20, 80])[0],)
    out = await shazam.recognize(data=audio_file, proxy=None)

    track_title = 0
    artist = 0
    album_cover = 0

    if "track" in out:
        if json == True:
            print(out)
        else:
            track_title = out["track"]["title"]
            artist = out["track"]["subtitle"]
            if "images" in out["track"]:
                album_cover = out["track"]["images"]["coverart"]
                # Forces the shazam image server to fetch a
                # high-resolution album cover.
                album_cover_hq = album_cover.replace(
                    "/400x400cc.jpg", "/1400x1400cc.png"
                )
            else:
                album_cover_hq = None

            # Writes CSV file.
            if write == True:
                if file_name is not None:
                    write_csv(
                        f"{file_name}", [timestamp, track_title, artist, album_cover_hq]
                    )
                else:
                    file_name = os.path.splitext(os.path.basename(audio_file))[0]
                    write_csv(
                        f"{file_name}", [timestamp, track_title, artist, album_cover_hq]
                    )

            print(f"Track: {track_title}")
            print(f"Artist: {artist}")
            print(f"Album Cover: {album_cover_hq}")
    else:
        print("No matches found.")


def split_and_identify(audio_file, duration=str):
    """
    Splits audio file by duration (seconds) and identifies songs. Writes the csv file automatically.

    :param audio_file: Path to audio file.
    :param duration: Length of each segment (seconds).
    """
    if not os.path.exists(audio_file):
        print(f"Error: File '{audio_file}' not found.")
        return

    file_name = os.path.splitext(os.path.basename(audio_file))[0]

    # Reads the audio file and calculates segment count.
    print(f"Reading {audio_file}...")
    data, samplerate = sf.read(audio_file)
    samples_per_duration = int(samplerate * duration)
    num_segments = len(data) // samples_per_duration

    with Progress() as progress:
        task = progress.add_task(
            "[green]Splitting and identifying audio...", total=num_segments
        )
        # Make each segment an audio file to be used in Shazamio.
        for i in range(num_segments):
            start_idx = i * samples_per_duration
            end_idx = start_idx + samples_per_duration
            segment_data = data[start_idx:end_idx]
            segment_time = start_idx / samplerate
            # Convert to HH:MM:SS format
            timestamp = datetime.utcfromtimestamp(segment_time).strftime("%H:%M:%S")
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
            # We need to slow down the process unless proxies are used.
            time.sleep(2)
