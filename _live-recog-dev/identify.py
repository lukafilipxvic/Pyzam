import asyncio
from shazamio import Shazam
import tempfile
import urllib.request


async def identify_audio(audio_file, json=False):
    # Start of shazam
    shazam = Shazam()
    out = await shazam.recognize_song(audio_file)

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
                    "/400x400cc.jpg", "/1000x1000cc.png"
                )  # convert link into HD album art

                urllib.request.urlretrieve(
                    album_cover_hq, "album_cover.png"
                )  # Download the album cover image from the URL

            else:
                album_cover_hq = None

            print("Track: ", track_title)
            print("Artist: ", artist)
            print("Album Cover: ", album_cover_hq)

    else:
        print("No matches found.")
