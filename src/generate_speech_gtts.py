#!/usr/bin/python3
# -*- coding: utf-8 -*-

# --- Script Summary ---
# Responsibility: Generate speech using Google Text-to-Speech (gTTS) API.
# Usage: python generate_speech_gtts.py <text> <outfile> [--lang LANG]
# Examples:
#   python generate_speech_gtts.py "Hello world" output.mp3
#   python generate_speech_gtts.py input.txt output.mp3 --lang es
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
# pip install gTTS
# pip install args_utils
#===============================================================================================================


import os
import sys
from gtts import gTTS
import args_utils

parser = args_utils.init_parser("Convert text to speech using Google TTS (Online).")
args_utils.add_text_arg(parser)
args_utils.add_outfile_arg(parser)
parser.add_argument("--lang", default="en", help="Language code (default: en)")
args = parser.parse_args()

# 1. Get Text
text = args_utils.get_text_content(args.text)

outfile = os.path.abspath(args.outfile)

# 2. Generate Audio
print("Connecting to Google TTS to convert text...")
try:
    tts = gTTS(text=text, lang=args.lang, slow=False)
    tts.save(outfile)
    print(f"Audio saved to: {outfile}")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)