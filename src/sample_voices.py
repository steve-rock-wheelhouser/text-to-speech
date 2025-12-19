#!/usr/bin/python3
# -*- coding: utf-8 -*-

# --- Script Summary ---
# Responsibility: Generate audio samples using specific Voice IDs (from voices.json) via Edge TTS.
# Usage: python sample_voices.py <text> <id1,id2,...> [--pitch PITCH] [--rate RATE] [--output-dir DIR]
# Examples:
#   python sample_voices.py "Hello world" "1,5,10" --output-dir samples
#   python sample_voices.py "Testing pitch" "12" --pitch="+50Hz"
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
# pip install edge-tts
#===============================================================================================================

import json
import os
import asyncio
import edge_tts
import args_utils

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VOICES_FILE = os.path.join(SCRIPT_DIR, "voices.json")

async def main():
    parser = args_utils.init_parser("Generate audio samples using Voice IDs.")
    args_utils.add_text_arg(parser)
    parser.add_argument("ids", help="Comma-separated list of Voice IDs (e.g. 1,5,10)")
    args_utils.add_pitch_rate_args(parser)
    parser.add_argument("--output-dir", default=".", help="Directory to save output files")
    args = parser.parse_args()

    if not os.path.exists(VOICES_FILE):
        print(f"Error: {VOICES_FILE} not found. Please run jsonify_voices.py first.")
        return

    with open(VOICES_FILE, "r", encoding="utf-8") as f:
        voices = json.load(f)

    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)

    # Create a lookup dictionary for ID -> Voice
    voice_map = {str(v.get("ID")): v for v in voices if "ID" in v}

    selected_ids = [x.strip() for x in args.ids.split(",")]

    print(f"Generating samples for IDs: {selected_ids}")

    text_content = args_utils.get_text_content(args.text)

    for vid in selected_ids:
        voice = voice_map.get(vid)
        if not voice:
            print(f"Skipping ID {vid}: Not found in voices.json")
            continue

        short_name = voice["ShortName"]
        # Create a filename like: sample_001_en-US-GuyNeural.mp3
        outfile = os.path.join(args.output_dir, f"sample_{vid.zfill(3)}_{short_name}.mp3")
        
        print(f"Generating {outfile} ({short_name})...")
        try:
            communicate = edge_tts.Communicate(text_content, short_name, pitch=args.pitch, rate=args.rate)
            await communicate.save(outfile)
        except Exception as e:
            print(f"Failed to generate {outfile}: {e}")

if __name__ == "__main__":
    asyncio.run(main())