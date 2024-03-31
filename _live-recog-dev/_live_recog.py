import asyncio
import record
from identify import identify_audio

# Run this to see song.
OUTPUT_FILENAME = "recorded_audio.wav"
RECORD_SEC = 5

# Record speaker and save audio
saved_file = record.speaker(
    OUTPUT_FILENAME, RECORD_SEC
)  # or record microphone using .microphone

if __name__ == "__main__":
    asyncio.run(identify_audio(saved_file))
