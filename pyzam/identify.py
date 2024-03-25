import asyncio
from shazamio import Shazam
import tempfile
import urllib.request


async def identify_audio(audio_file):
    # Start of shazam
    shazam = Shazam()
    out = await shazam.recognize(audio_file)

    track_title = 0
    artist = 0
    album_cover = 0

    if "track" in out:
        if out["track"]["title"] != track_title:
            track_title = out["track"]["title"]
        if out["track"]["subtitle"] != artist:
            artist = out["track"]["subtitle"]
        if "images" in out["track"]:
            if out["track"]["images"]["coverart"] != album_cover:
                album_cover = out["track"]["images"]["coverart"]
                album_cover_hq = album_cover.replace(
                    "/400x400cc.jpg", "/1000x1000cc.png"
                )  # convert link into HD album art

                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                    urllib.request.urlretrieve(album_cover_hq, temp_file.name)  # Download the album cover image from the URL

        else:
            album_cover_hq = "NA found."

        print("Track: ", track_title)
        print("Artist: ", artist)
        print("Album Cover: ", album_cover_hq)

    else:
        print("No song was found.")
