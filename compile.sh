#!/bin/bash

echo "--- Setting up PyInstaller Environment ---"
source .venv/bin/activate
pip install pyinstaller

echo "--- Cleaning previous builds ---"
rm -rf build

echo "--- Building with PyInstaller ---"
# --onefile: Create a single executable
# --windowed: Do not show a console window when running
# --add-data: Bundle the assets folder (format is source:dest)
pyinstaller --noconfirm --onefile --windowed \
    --name "text-to-speech" \
    --icon "assets/icons/icon.png" \
    --add-data "assets:assets" \
    --add-data "voice-library:voice-library" \
    --add-data "src/voices.json:." \
    src/text_to_speech.py

if [ -f "dist/text-to-speech" ]; then
    echo "--- Success! Binary created: dist/text-to-speech ---"
    # Play success sound (replace with your MP3 player and file)
    mpg123 ~/projects/audio-files/compilation_great_success.mp3
else
    echo "--- Build failed ---"
    # Play fail sound (replace with your MP3 player and file)
    mpg123 ~/projects/audio-files/compilation_failed_yet_again.mp3
fi