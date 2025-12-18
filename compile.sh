#!/bin/bash
set -e

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
    src/text_to_speech.py

echo "--- Success! Binary created: dist/text-to-speech ---"

# Play a notification sound (System Bell) to alert the user
echo -e "\a"