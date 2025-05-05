<br />
<p align="center">
<img src="https://github.com/lukafilipxvic/pyzam/blob/main/images/pyzam-logo-dark.png?raw=true#gh-light-mode-only" alt="Pyzam logo" width="459">
<img src="https://github.com/lukafilipxvic/pyzam/blob/main/images/pyzam-logo-light.png?raw=true#gh-dark-mode-only" alt="Pyzam logo" width="459">
</p>
<br />
<br />

<p align="center">
  <a href="./LICENSE.md"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <a href="https://pypi.org/project/pyzam/"><img src="https://img.shields.io/pypi/v/pyzam.svg"></a>
  <img src="https://pepy.tech/badge/pyzam" alt="https://pepy.tech/project/pyzam">
  <img src="https://pepy.tech/badge/pyzam/month" alt="https://pepy.tech/project/pyzam">  
</p>

Pyzam is a free CLI music recognition tool for audio and mixtapes in Python.

<p align="center">
  <img src="https://github.com/lukafilipxvic/pyzam/blob/main/images/pyzam-usage.gif" alt="Pyzam usage", width"459">
</p>

## Installation

### Dependencies
Pyzam requires [ffmpeg](https://git.ffmpeg.org/ffmpeg.git 'Download ffmpeg') installed.

### Installation
Using uv (recommended):
```bash
uv tool run pyzam --speaker
```

Using pip:
```bash
$ pip install pyzam
```

Using environment.yml with Conda (installs ffmpeg for you):
```
conda env create -n pyzam --file=environment.yml

conda activate pyzam
```

## Usage
Using uv:
```bash
uv tool run pyzam --speaker
```
Using pip:
```bash
# Listen to speaker (5 seconds by default)
pyzam --speaker

# Listen to microphone
pyzam --microphone

# Listen to audio files
pyzam --input audio_file.mp3

# Listen to audio via URL
pyzam --url "https://archive.org/download/09-hold-me-in-your-arms/02%20-%20Never%20Gonna%20Give%20You%20Up.mp3"
```

```bash
# Loop the recognition continously and save the logs as CSV file
pyzam --speaker -d 10 --write --loop

# Listen to mixtapes and save the logs as CSV file
pyzam --input audio_file.mp3 --duration 12 --mixtape
```

See `pyzam --help` for more options.

## Options
| Argument name     | Description                                          |
| ----------------  | -----------------------------------------------------|
| --input           | Detects from the given audio input file.
| --microphone, -m  | Listens to the microphone of your device.
| --speaker, -s     | Listens to the speaker of your device (default).
| --url, -u         | Detects from the given URL to an audio file.
| --help, -h        | Show usage, options and exit.
| --duration, -d    | Length of microphone or speaker recording. Max = 12 seconds.
| --quiet, -q       | Supresses the operation messages (i.e. Recording speaker for X seconds...). 
| --loop, -l        | Loop the recognition process indefinitely.
| --mixtape         | Detects every -d seconds for a given input file, only works with --input. --write is enabled automatically.
| --json, -j        | Return the whole Shazamio output in JSON.
| --write, -w       | Writes the output of as a CSV file.


## Known Limitations
### Shazam API Call Limit (Error 429)
Shazam allows up to 20 requests per minute. Hence, a proxy is recommended to speed up recognition when using ```--mixtape```.

### 12 Second Duration Limit per request
The maximum sample duration that Shazam allows is 12 seconds. Any audio after 12 seconds will not be recieved by Shazam. 
