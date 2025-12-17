# Text-to-Speech Project

A collection of Python scripts for generating, managing, and reviewing text-to-speech audio using various engines, including Microsoft Edge TTS (high quality), Google TTS, and offline system engines (espeak/pyttsx3).

## Features

*   **High-Quality TTS**: Use Microsoft Edge's online neural voices.
*   **Offline Support**: Fallback to system TTS engines like `espeak` or `pyttsx3`.
*   **Google TTS**: Support for Google's gTTS API.
*   **Batch Processing**: Generate samples for multiple voices or specific genders in bulk.
*   **Review Tools**: Interactively play, save, or reject generated audio samples.
*   **Robust Playback**: A custom audio player that handles various environments (Linux, Flatpak, macOS).

## Setup

### 1. Environment Setup
It is recommended to use a virtual environment.

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### 2. Install Dependencies
Install the required Python packages:

```bash
pip install edge-tts gTTS pyttsx3 pygame
```

*Note: `args_utils.py` is a local utility module included in this project and does not need to be installed via pip.*

### 3. System Dependencies (Linux)
For offline generation and audio playback, you may need system packages:
```bash
# Fedora/RHEL
sudo dnf install espeak-ng python3-devel

# Ubuntu/Debian
sudo apt-get install espeak-ng python3-dev
```

## Script Usage

### Speech Generation

#### `generate_speech_edge.py`
Generates high-quality speech using Microsoft Edge TTS.
```bash
# Generate audio
python generate_speech_edge.py "Hello world" output.mp3 --voice en-US-GuyNeural

# List available voices
python generate_speech_edge.py --list-voices
```

#### `generate_speech_gtts.py`
Generates speech using Google Text-to-Speech (Online).
```bash
python generate_speech_gtts.py "Hello world" output.mp3
python generate_speech_gtts.py input.txt output.mp3 --lang es
```

#### `generate_speech.py`
Generates offline speech using `pyttsx3` or `espeak`. Useful for environments without internet.
```bash
python generate_speech.py "Hello world" output.wav
python generate_speech.py input.txt output.wav
```

### Batch Processing & Sampling

#### `batch_generate.py`
Generates audio samples for all voices of a specific gender found in `voices.json`.
```bash
python batch_generate.py Male "Hello there" ./male_samples
python batch_generate.py Female "Testing speed" ./female_fast --rate="+20%"
```

#### `sample_voices.py`
Generates audio samples for specific Voice IDs (referenced from `voices.json`).
```bash
python sample_voices.py "Hello world" "1,5,10" --output-dir samples
python sample_voices.py "Testing pitch" "12" --pitch="+50Hz"
```

### Utilities & Tools

#### `play_audio.py`
A robust command-line audio player. Tries Pygame first, then falls back to system players (`paplay`, `aplay`, `afplay`, `ffplay`).
```bash
python play_audio.py output.mp3
```

#### `review_samples.py`
Interactively review audio files in a directory. Plays files and lets you sort them into 'saved' or 'rejected' folders.
```bash
python review_samples.py ./samples
python review_samples.py ./output --saved-folder keepers --rejected-folder trash
```

#### `jsonify_voices.py`
Reads `voices.json` and adds sequential IDs to each voice entry for easier referencing by other scripts.
```bash
python jsonify_voices.py
```

## License

This project is licensed under the GNU General Public License v3.0.

Copyright (C) 2025 steve.rock@wheelhouser.com
```