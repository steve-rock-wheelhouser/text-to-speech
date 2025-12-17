#!/usr/bin/python3
# -*- coding: utf-8 -*-

# --- Script Summary ---
# Responsibility: Generate offline speech using pyttsx3/espeak. Handles Flatpak/Linux environment issues.
# Usage: python generate_speech.py <text> <outfile>
# Examples:
#   python generate_speech.py "Hello world" output.wav
#   python generate_speech.py input.txt output.wav
# ----------------------

# Copyright (C) 2025 steve.rock@wheelhouser.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# --- Setup Instructions ---
# Active the venv on linux/macOS:
# python -m venv .venv
# source .venv/bin/activate
# pip install --upgrade pip
# pip install pyttsx3
# pip install args_utils
#===============================================================================================================


import pyttsx3
import subprocess
import os
import sys
import shutil
import args_utils

parser = args_utils.init_parser("Convert text to speech.")
args_utils.add_text_arg(parser)
args_utils.add_outfile_arg(parser)
args = parser.parse_args()

text = args_utils.get_text_content(args.text)
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
