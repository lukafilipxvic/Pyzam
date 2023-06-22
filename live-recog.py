import asyncio
import soundcard as sc
import soundfile as sf
import urllib.request
from shazamio import Shazam

def record_audio(filename, seconds, rate):
    print(f"* Recording speaker for {seconds} seconds.")

    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=rate) as mic:
        # record audio with loopback from default speaker.
        data = mic.record(numframes=rate*seconds)
        
        # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
        sf.write(file=filename, data=data[:, 0], samplerate=rate)

    print("* Audio recording finished.")

    return filename

async def main():
    OUTPUT_FILENAME = 'recorded_audio.wav'
    RECORD_SEC = 5
    RATE = 44100

    loop = True

    while loop:
        # Record and save audio
        saved_file = record_audio(OUTPUT_FILENAME, RECORD_SEC, RATE)

        # Start of shazam
        shazam = Shazam()
        out = await shazam.recognize_song(saved_file)

        if 'track' in out:
            track_title = out['track']['title']
            artist = out['track']['subtitle']

            if 'images' in out['track']:
                album_cover = out['track']['images']['coverart']
                album_cover_hq = album_cover.replace('/400x400cc.jpg', '/1000x1000cc.png') # convert link into HD album art

                urllib.request.urlretrieve(album_cover_hq, 'album_cover.png') # Download the album cover image from the URL

            else:
                album_cover_hq = 'NA found.'

            print("Track: ", track_title)
            print("Artist: ", artist)
            print("Album Cover: ", album_cover_hq)


        else:
            print("No song was found.")

        # Ask the user if they want to loop
        user_input = input("Do you want run again? (y/n): ")
        if user_input.lower() != 'y':
            loop = False

asyncio.run(main())