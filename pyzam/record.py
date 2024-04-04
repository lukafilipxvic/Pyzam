import soundcard as sc
import soundfile as sf


def speaker(filename: str, seconds):
    """
    Records the device's speaker.

    :param filename: Name of audio file written.
    :param seconds: Duration to record (seconds).
    """
    with sc.get_microphone(
        id=str(sc.default_speaker().name), include_loopback=True
    ).recorder(samplerate=44100) as speaker:
        print(f"Recording speaker for {seconds} seconds...")

        data = speaker.record(numframes=44100 * seconds)
        sf.write(file=filename, data=data, samplerate=44100)
    return filename


def microphone(filename: str, seconds):
    """
    Records the device's device.

    :param filename: Name of audio file written.
    :param seconds: Duration to record (seconds).
    """
    with sc.get_microphone(
        id=str(sc.default_microphone().name), include_loopback=True
    ).recorder(samplerate=44100) as mic:
        print(f"Recording microphone for {seconds} seconds...")
        data = mic.record(numframes=44100 * seconds)
        sf.write(file=filename, data=data, samplerate=44100)
    return filename
