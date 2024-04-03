import asyncio
from shazamio import Shazam


async def main():
    shazam = Shazam()
    out = await shazam.recognize("_file-recog-dev/recorded_audio.wav")

    if "track" in out:
        track_title = out["track"]["title"]
        artist = out["track"]["subtitle"]

        if "images" in out["track"]:
            album_cover = out["track"]["images"]["coverart"]
            album_cover_hq = album_cover.replace(
                "/400x400cc.jpg", "/1000x1000cc.png"
            )  # convert link into HD album art
        else:
            album_cover_hq = "NA found."

        print("Track: ", track_title)
        print("Artist: ", artist)
        print("Album Cover: ", album_cover_hq)

    else:
        print("No song was found.")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
