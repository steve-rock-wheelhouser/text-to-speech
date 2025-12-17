#!/usr/bin/python3
# -*- coding: utf-8 -*-

# --- Fedora Setup Instructions ---
# Active the venv on linux/macOS:
# python -m venv .venv
# source .venv/bin/activate
# # Install system dependencies:
# sudo dnf install espeak-ng
# # If pyttsx3 fails to find espeak, create this symlink:
# # sudo ln -s /usr/lib64/libespeak-ng.so.1 /usr/lib64/libespeak.so.1
# pip install --upgrade pip
# pip install pyttsx3

import argparse
import pyttsx3
import subprocess
import os
import sys
import shutil

parser = argparse.ArgumentParser(description="Convert text to speech.")
parser.add_argument("text", help="The text to convert to speech")
parser.add_argument("outfile", help="The output file path (e.g. output.wav)")
args = parser.parse_args()

if os.path.isfile(args.text):
    with open(args.text, "r", encoding="utf-8") as f:
        text = f.read()
else:
    text = args.text
outfile = os.path.abspath(args.outfile)

try:
    engine = pyttsx3.init()
    print(f"Processing text: '{text}'")
    engine.save_to_file(text, outfile)
    engine.runAndWait()

    if not os.path.exists(outfile) or os.path.getsize(outfile) == 0:
        raise RuntimeError("pyttsx3 failed to generate audio file")

    print(f"Audio saved to: {outfile}")
except (RuntimeError, KeyError, OSError):
    print("Warning: pyttsx3 driver failed. Falling back to system command.")
    # Find the espeak executable explicitly
    cmd = shutil.which("espeak-ng") or shutil.which("espeak")

    # If not found in PATH, check standard locations
    if not cmd:
        for path in ["/usr/bin/espeak-ng", "/usr/bin/espeak", "/usr/local/bin/espeak-ng", "/usr/local/bin/espeak"]:
            if os.path.exists(path) and os.access(path, os.X_OK):
                cmd = path
                break

    if cmd:
        subprocess.run([cmd, "-w", outfile], input=text, text=True, check=True)
        print(f"Audio saved to: {outfile}")
    elif shutil.which("flatpak-spawn"):
        print("Detecting Flatpak environment. Attempting to run on host...")
        subprocess.run(["flatpak-spawn", "--host", "espeak-ng", "-w", outfile], input=text, text=True, check=True)
        print(f"Audio saved to: {outfile}")
    else:
        print("Error: Neither 'espeak-ng' nor 'espeak' found in PATH or standard locations.")
        print(f"Current PATH: {os.environ.get('PATH')}")
        sys.exit(1)