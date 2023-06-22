import streamlit as st
import wave
import pyaudio
import urllib.request
import asyncio
from shazamio import Shazam

st.set_page_config(
    layout="centered",
    page_title="Song Identifier",
    page_icon="🔎",
)

col1, col2 = st.columns([1, 1], gap="small")

with st.sidebar:
    st.title("Song Identifier 🔎🎵")


async def recognize_song():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 4
    WAVE_OUTPUT_FILENAME = 'recorded_audio.wav'

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* Recording audio input for 4 seconds")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    print("* Audio recording finished.")

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Start of shazam
    shazam = Shazam()
    out = await shazam.recognize_song(WAVE_OUTPUT_FILENAME)

    if 'track' in out:
        track_title = out['track']['title']
        artist = out['track']['subtitle']

        col1.header("Now playing: " + track_title)  # Display information
        col1.header("By: " + artist)

        if 'images' in out['track']:
            album_cover = out['track']['images']['coverart']
            print(album_cover)
            album_cover_hq = album_cover.replace(
                '/400x400cc.jpg', '/1000x1000cc.png')  # convert link into HD album art

            # Download the album cover image from the URL
            urllib.request.urlretrieve(album_cover_hq, 'album_cover.png')
            col2.image(urllib.request.urlopen(
                album_cover_hq).read(), width=300)

        else:
            album_cover_hq = 'NA found.'
            col2.image('album_default.png', width=300)

        print("Track: ", track_title)
        print("Artist: ", artist)
        print("Album Cover: ", album_cover_hq)

    else:
        st.text("No song was found.")

# Run button in the sidebar
if st.sidebar.button('Start Recognition'):
    col1.empty()
    col2.empty()
    asyncio.run(recognize_song())

hide_streamlit_style = """
                <style>
                footer {visibility: hidden;
                }
                #MainMenu {visibility: hidden;
                # }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
