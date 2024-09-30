import requests
import soundcard as sc
import soundfile as sf
import io

def speaker(filename: str, seconds, quiet=False):
    """
    Records the device's speaker.

    :param filename: Name and directory of the audio file written.
    :param seconds: Duration to record (seconds).
    :param quiet: If True, suppresses print statements.
    """
    speaker = sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True)
    with speaker.recorder(samplerate=44100) as speaker_recorder:
        if not quiet:
            print()
            print(f"Recording {speaker.name} for {seconds} seconds...")

        data = speaker_recorder.record(numframes=44100 * seconds)
        sf.write(file=filename, data=data, samplerate=44100)
    return filename


def microphone(filename: str, seconds, quiet=False):
    """
    Records the device's microphone.

    :param filename: Name and directory of the audio file written.
    :param seconds: Duration to record (seconds).
    :param quiet: If True, suppresses recording statements.
    """
    mic = sc.default_microphone()
    with mic.recorder(samplerate=44100) as mic_recorder:
        if not quiet:
            print()
            print(f"Recording {mic.name} for {seconds} seconds...")

        data = mic_recorder.record(numframes=44100 * seconds)
        sf.write(file=filename, data=data, samplerate=44100)
    return filename


def url(url: str, filename: str, quiet=False):
    """
    Downloads audio from the provided URL.

    :param url: URL of the audio file.
    :param filename: Name and directory of the audio file written.
    :param quiet: If True, suppresses print statements.
    """
    if not quiet:
        print(f"Downloading audio from URL...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if code is 4XX/5XX

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return None
    except Exception as err:
        print(f'An error occurred: {err}')
        return None

    # Ensure the response content is in a suitable format for soundfile
    data, samplerate = sf.read(io.BytesIO(response.content))
    sf.write(file=filename, data=data, samplerate=samplerate)
    return filename