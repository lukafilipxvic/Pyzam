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

Pyzam is a free CLI music recognition tool in Python.

## Installation

### Dependencies
Pyzam requires [ffmpeg](https://git.ffmpeg.org/ffmpeg.git 'Download ffmpeg') installed.

### Installation
```bash
$ pip install git+https://github.com/lukafilipxvic/Pyzam.git#egg=Pyzam

```


## Usage
```bash
# Pyzam listen to speaker for 5 seconds by default
pyzam --speaker

# Listen to microphone
pyzam --microphone
```

```bash
# Pyzam
pyzam --input audio_file.mp3
```

See `pyzam --help` for more options.

## Options
| Argument name     | Description                                          |
| ----------------  | -----------------------------------------------------|
| --speaker, -s     | Listens to the speaker of your device (default)
| --microphone, -m  | Listens to the microphone of your device
| --help, -h        | Show Usage & Options and exit
| --duration, -d    | Length of microphone or speaker recording
| --input           | Detect from the given audio input file
| --json, -j        | Return the whole Shazam output in json
