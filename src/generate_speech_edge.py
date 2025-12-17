#!/usr/bin/python3
# -*- coding: utf-8 -*-

# --- Script Summary ---
# Responsibility: Generate high-quality speech using Microsoft Edge TTS. Can also list available voices.
# Usage: python generate_speech_edge.py <text> <outfile> [--voice VOICE_ID] [--list-voices] [--json] [--play] [--pitch PITCH] [--rate RATE]
# Examples:
#   python generate_speech_edge.py "Always with you, what can't be done" output.mp3 --voice en-US-GuyNeural --pitch="-10Hz" --rate="-35%" --play
#   python generate_speech_edge.py --list-voices
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
# pip install args_utils
#===============================================================================================================


import json
import asyncio
import os
import sys
import edge_tts
import args_utils

# Ensure we can import play_audio from the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from play_audio import play_audio

async def main():
    parser = args_utils.init_parser("Convert text to speech using Microsoft Edge TTS (High Quality).")
    args_utils.add_text_arg(parser, required=False)
    args_utils.add_outfile_arg(parser, required=False)
    parser.add_argument("--voice", default="en-US-AriaNeural", help="Voice ID (default: en-US-AriaNeural)")
    parser.add_argument("--list-voices", action="store_true", help="List available voices and exit")
    parser.add_argument("--json", action="store_true", help="Output voices as JSON (use with --list-voices)")
    args_utils.add_pitch_rate_args(parser)
    args_utils.add_volume_arg(parser)
    parser.add_argument("--play", action="store_true", help="Automatically play the generated audio")
    args = parser.parse_args()

    if args.list_voices:
        voices = await edge_tts.list_voices()
        if args.json:
            for i, v in enumerate(voices, 1):
                v['ID'] = i
            print(json.dumps(voices, indent=2))
            return
        for v in voices:
            print(f"{v['ShortName']} ({v['Gender']}) - {v['Locale']}")
        return

    if not args.text or not args.outfile:
        parser.print_help()
        sys.exit(1)

    # 1. Get Text
    text = args_utils.get_text_content(args.text)

    outfile = os.path.abspath(args.outfile)

    # 2. Generate Audio
    print("Connecting to Edge TTS...")
    print(f"Voice: {args.voice}")
    print(f"Params: Pitch={args.pitch}, Rate={args.rate}, Volume={args.volume}")
    
    try:
        communicate = edge_tts.Communicate(text, args.voice, pitch=args.pitch, rate=args.rate, volume=args.volume)
        await communicate.save(outfile)
        print(f"Audio saved to: {outfile}")

        if args.play:
            play_audio(outfile)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
