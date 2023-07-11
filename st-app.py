import streamlit as st
import asyncio
import soundcard as sc
import soundfile as sf
import urllib.request
from shazamio import Shazam
from streamlit_autorefresh import st_autorefresh


st.set_page_config(
    layout="centered",
    page_title="Song Identifier",
    page_icon="🔎",
)


col1, col2 = st.columns([1, 1], gap="small")

with st.sidebar:
    st.title("Song Identifier 🔎🎵")


def record_audio(filename, seconds, rate):
    print(f"* Recording speaker for {seconds} seconds.")

    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=rate) as mic:
        # record audio with loopback from default speaker.
        data = mic.record(numframes=rate*seconds)
        
        # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
        sf.write(file=filename, data=data[:, 0], samplerate=rate)

    print("* Audio recording finished.")

    return filename

async def recog_song():
    OUTPUT_FILENAME = 'recorded_audio.wav'
    RECORD_SEC = 4
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
                print(album_cover)
                album_cover_hq = album_cover.replace('/400x400cc.jpg', '/1000x1000cc.png') # convert link into HD album art

                # Download the album cover image from the URL
                urllib.request.urlretrieve(album_cover_hq, 'album_cover.png') # Download the album cover image from the URL

                col1.header("Now playing: " + track_title)
                col1.header("By: " + artist) 
                col2.image(urllib.request.urlopen(album_cover_hq).read(), width=300)

            else:
                album_cover_hq = 'NA found.'
                col1.header("Now playing: " + track_title)
                col1.header("By: " + artist) 
                col2.image('album_default.png', width=300)

            print("Track: ", track_title)
            print("Artist: ", artist)
            print("Album Cover: ", album_cover_hq)


        else:
            col1.header("No song was found.")
            col2.image('album_default.png', width=300)


if st.sidebar.button('Start Recognition'):
    asyncio.run(recog_song())


hide_streamlit_style = """
                <style>
                footer {visibility: hidden;
                }
                #MainMenu {visibility: hidden;
                # }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
