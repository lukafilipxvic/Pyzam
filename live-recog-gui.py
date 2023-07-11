import asyncio
import soundcard as sc
import soundfile as sf
import urllib.request
from shazamio import Shazam
import tkinter as tk
from PIL import ImageTk, Image

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
    RECORD_SEC = 4
    RATE = 44100

    for i in range(5):
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

            # Create a tkinter window to display the printed items and album cover
            window = tk.Tk()
            window.title("Song Recognition")
            window.geometry("500x500")

            # Display the track title and artist
            track_label = tk.Label(window, text="Track: " + track_title)
            track_label.pack()

            artist_label = tk.Label(window, text="Artist: " + artist)
            artist_label.pack()

            # Display the album cover
            if 'images' in out['track']:
                img = Image.open("album_cover.png")
            else:
                img = Image.open("album_default.png")
            img = img.resize((300, 300), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            panel = tk.Label(window, image=img)
            panel.image = img
            panel.pack()

            # Run the UI
            window.mainloop()

        else:
            print("No song was found.")

asyncio.run(main())