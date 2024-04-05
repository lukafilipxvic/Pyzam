<br />
<p align="center">
<img src="https://github.com/lukafilipxvic/pyzam/blob/main/images/pyzam-logo-dark.png?raw=true#gh-light-mode-only" alt="Pyzam logo" width="459">
<img src="https://github.com/lukafilipxvic/pyzam/blob/main/images/pyzam-logo-light.png?raw=true#gh-dark-mode-only" alt="Pyzam logo" width="459">
</p>
<br />
<br />

<p align="center">
  <a href="./LICENSE.md"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
</p>

Pyzam is a free CLI music recognition tool for audio and mixtapes in Python.

## Installation

### Dependencies
Pyzam requires [ffmpeg](https://git.ffmpeg.org/ffmpeg.git 'Download ffmpeg') installed.

### Installation
```bash
$ pip install git+https://github.com/lukafilipxvic/Pyzam.git#egg=Pyzam

```


## Usage
```bash
# Listen to speaker (5 seconds by default)
pyzam --speaker

# Listen to microphone
pyzam --microphone

# Listen to audio files
pyzam --input audio_file.mp3
```

```bash
# Loop the recognition continously
pyzam --speaker -d 10 --loop

# Listen to mixtapes and save record log as csv file
pyzam --input audio_file.mp3 --duration 12 --mixtape
```

See `pyzam --help` for more options.

## Options
| Argument name     | Description                                          |
| ----------------  | -----------------------------------------------------|
| --input           | Detects from the given audio input file
| --microphone, -m  | Listens to the microphone of your device
| --speaker, -s     | Listens to the speaker of your device (default)
| --help, -h        | Show usage & options and exit
| --duration, -d    | Length of microphone or speaker recording. Max = 12 seconds.
| --loop, -l        | Loop the recognition process indefinitely
| --mixtape         | Detects every -d seconds for a given input file, only works with --input. --write is enabled automatically.
| --json, -j        | Return the whole Shazamio output in json
| --write, -w       | Writes the output of as a csv file


## Known Limitations
### Shazam API Call Limit (Error 429)
Shazam allows up to 20 requests per minute. Hence, a proxy is recommended to speed up recognition when using ```--mixtape```.

### 12 Second Sample Limit per request
The maximum sample duration that Shazam allows is 12 seconds. Any audio after 12 seconds will not be recieved by Shazam. 