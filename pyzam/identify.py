import asyncio
import csv
from datetime import datetime
from rich.progress import Progress
from shazamio import Shazam
import soundfile as sf
import tempfile
import time
import os


def write_csv(
    file_name=str, timestamp=str, track_title=str, artist=str, album_cover=str
):
    """
    Writes the song's data into a csv file.
    """
    file_exists = os.path.isfile(f"{file_name}.csv")

    with open(f"{file_name}.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Track", "Artist", "Album Cover"])
        writer.writerow([timestamp, track_title, artist, album_cover])


async def identify_audio(audio_file=str, json=False, write=False, timestamp=None, file_name=None):
    """
    Identifies the song of a given audio file.
    Timestamp if write is True.
    file_name is set to "track_info_{audio_file}" if none is provided. This is used in split_and_identify (mixtape).
    """
    if not os.path.exists(audio_file):
        print(f"Error: File '{audio_file}' not found.")
        return
    shazam = Shazam()
    out = await shazam.recognize(audio_file)

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
                album_cover_hq = album_cover.replace(
                    "/400x400cc.jpg", "/1400x1400cc.png"
                )
            else:
                album_cover_hq = None

            if write == True:
                if file_name is not None:
                    write_csv(f'{file_name}', timestamp, track_title, artist, album_cover_hq)
                else:
                    file_name = os.path.splitext(os.path.basename(audio_file))[0]
                    write_csv(f'track_info_{file_name}', timestamp, track_title, artist, album_cover_hq)

            print(f"Track: {track_title}")
            print(f"Artist: {artist}")
            print(
                f"Album Cover: {album_cover_hq}"
            )

    else:
        print("No matches found.")


def split_and_identify(audio_file, duration=str):
    """
    Splits a given audio file by the given duration and identifies the songs. Writes the csv file automatically.
    """
    if not os.path.exists(audio_file):
        print(f"Error: File '{audio_file}' not found.")
        return

    file_name = os.path.splitext(os.path.basename(audio_file))[0]

    data, samplerate = sf.read(audio_file)
    samples_per_duration = int(samplerate * duration)
    num_segments = len(data) // samples_per_duration

    with Progress() as progress:
        task = progress.add_task(
            "[green]Splitting and identifying audio...", total=num_segments
        )
        for i in range(num_segments):
            start_idx = i * samples_per_duration
            end_idx = start_idx + samples_per_duration
            segment_data = data[start_idx:end_idx]
            segment_time = start_idx / samplerate
            timestamp = datetime.utcfromtimestamp(segment_time).strftime(
                "%H:%M:%S"
            )  # Convert to MM:SS format
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
            progress.update(task, advance=1)
            time.sleep(2)  #  to slowdown and avoid shazamio call limits.
