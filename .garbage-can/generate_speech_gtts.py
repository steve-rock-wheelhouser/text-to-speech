#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Install dependency:
# pip install gTTS
# source .venv/bin/activate

import argparse
import os
import sys
from gtts import gTTS

parser = argparse.ArgumentParser(description="Convert text to speech using Google TTS (Online).")
parser.add_argument("text", help="The text to convert or path to a text file")
parser.add_argument("outfile", help="The output file path (e.g. output.mp3)")
parser.add_argument("--lang", default="en", help="Language code (default: en)")
args = parser.parse_args()

# 1. Get Text
if os.path.isfile(args.text):
    with open(args.text, "r", encoding="utf-8") as f:
        text = f.read()
else:
    text = args.text

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