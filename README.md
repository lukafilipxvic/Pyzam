# Pyzam

<p align="center">
  <a href="./LICENSE.md"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
</p>

Pyzam is a free CLI music recognition tool using python.

## Installation

### Dependencies
'Pyzam' requires [ffmpeg](https://git.ffmpeg.org/ffmpeg.git 'Download ffmpeg')

```bash
$ pip install 
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
pyzam --input audio.mp3

# ...which can be overriden
pyzam --input audio.mp3 --duration 10
```

See `pyzam --help` for more options.

## Options
| Argument name     | Description                                          |
| ----------------  | -----------------------------------------------------|
| --speaker, -s     | Listens to the speaker of your device (by default).
| --microphone, -m  | Listens to the microphone of your device
| --help, -h        | Show Usage & Options and exit.   
