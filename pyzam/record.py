import soundcard as sc
import soundfile as sf


def speaker(filename, seconds):
    print(f"* Recording speaker for {seconds} seconds.")

    with sc.get_microphone(
        id=str(sc.default_speaker().name), include_loopback=True
    ).recorder(samplerate=44100) as mic:
        data = mic.record(
            numframes=44100 * seconds
        )  # record audio with loopback from default speaker.
        sf.write(
            file=filename, data=data[:, 0], samplerate=44100
        )  # remove [:, 0] to write audio as multiple-channels.

    print("* Audio recording finished.")
    return filename


def microphone(filename, seconds):
    print(f"* Recording microphone for {seconds} seconds.")

    with sc.get_microphone(
        id=str(sc.default_microphone().name), include_loopback=True
    ).recorder(samplerate=44100) as mic:
        data = mic.record(numframes=44100 * seconds)
        sf.write(file=filename, data=data[:, 0], samplerate=44100)

    print("* Audio recording finished.")
    return filename