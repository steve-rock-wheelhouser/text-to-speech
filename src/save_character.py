#!/usr/bin/python3
# -*- coding: utf-8 -*-

# --- Script Summary ---
# Responsibility: Create a new character entry in voice-library/characters.json.
# Usage: python save_character.py --alias "Name" --voice-id ID [options]
# Examples:
#   python src/save_character.py --alias "Yoda" --voice-id 210 --settings voice-library/always-with-you-what-cant-be-done/settings.json
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
# pip install pygame
#===============================================================================================================

import json
import os
import sys
import re
import args_utils

VOICES_FILE = "/home/user/projects/Text-to-Speech/src/voices.json"
LIBRARY_FILE = "/home/user/projects/Text-to-Speech/voice-library/characters.json"

# Offsets relative to the "Calm" (Baseline) settings
# Format: (Rate Offset, Pitch Offset, Volume Offset, Style)
VARIATION_TEMPLATES = {
    "Calm":         (0, 0, 0, "general"),
    "Excited":      (10, 2, 5, "cheerful"),
    "Stressed":     (10, 5, 10, "unfriendly"),
    "Whisper":      (-10, 0, -20, "whispering"),
    "Angry":        (15, 0, 20, "angry"),
    "Loud":         (0, 0, 30, "shouting"),
    "Depressed":    (-15, -5, -10, "sad"),
    "Frustrated":   (5, 5, 10, "unfriendly"),
    "Cheerful":     (10, 5, 5, "cheerful"),
    "Inside Voice": (-5, -5, -15, "general"),
    "Desperate":    (20, 15, 15, "terrified")
}

def parse_val(s):
    """Parses a string like '+10%' or '-5Hz' into (number, unit)."""
    if not s:
        return 0, ""
    m = re.match(r"([+-]?\d+)(.*)", s)
    if m:
        return int(m.group(1)), m.group(2)
    return 0, ""

def apply_offset(base_s, offset):
    """Applies an integer offset to a value string."""
    val, unit = parse_val(base_s)
    new_val = val + offset
    sign = "+" if new_val >= 0 else ""
    return f"{sign}{new_val}{unit}"

def main():
    parser = args_utils.init_parser("Add a new character to the library.")
    parser.add_argument("--alias", required=True, help="Character Alias (e.g. 'Narrator - Deep')")
    parser.add_argument("--voice-id", required=True, help="ID from voices.json")
    parser.add_argument("--description", default="", help="Description of the character")
    parser.add_argument("--sample-text", default="Hello, I am ready to speak.", help="Default sample text")
    parser.add_argument("--engine", default="edge-tts", help="TTS Engine (default: edge-tts)")
    parser.add_argument("--settings", help="Path to a settings.json file (or directory) to load pitch/rate from")
    
    # Baseline settings (Calm)
    args_utils.add_pitch_rate_args(parser)
    args_utils.add_volume_arg(parser)
    
    args = parser.parse_args()

    # 0. Load Settings from File if provided
    if args.settings:
        settings_path = args.settings
        if os.path.isdir(settings_path):
            settings_path = os.path.join(settings_path, "settings.json")
            
        if os.path.exists(settings_path):
            print(f"Loading settings from {settings_path}...")
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings_data = json.load(f)
                args.pitch = settings_data.get("pitch", args.pitch)
                args.rate = settings_data.get("rate", args.rate)
                args.volume = settings_data.get("volume", args.volume)
                args.sample_text = settings_data.get("text", args.sample_text)
        else:
            print(f"Warning: Settings file not found at {settings_path}")

    # 1. Load Voice Data
    if not os.path.exists(VOICES_FILE):
        print(f"Error: {VOICES_FILE} not found.")
        sys.exit(1)

    with open(VOICES_FILE, 'r', encoding='utf-8') as f:
        voices = json.load(f)

    # Find voice by ID
    voice_data = next((v for v in voices if str(v.get('ID')) == str(args.voice_id)), None)
    if not voice_data:
        print(f"Error: Voice ID {args.voice_id} not found in voices.json.")
        sys.exit(1)

    # 2. Load or Initialize Library
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, 'r', encoding='utf-8') as f:
            try:
                library = json.load(f)
            except json.JSONDecodeError:
                library = []
    else:
        os.makedirs(os.path.dirname(LIBRARY_FILE), exist_ok=True)
        library = []

    # 3. Determine ReferenceID
    next_id = 1
    if library:
        next_id = max(c.get("ReferenceID", 0) for c in library) + 1

    # 4. Generate Variations
    variations = {}
    
    print(f"Generating variations based on baseline: Rate={args.rate}, Pitch={args.pitch}, Vol={args.volume}")

    for name, (rate_off, pitch_off, vol_off, style) in VARIATION_TEMPLATES.items():
        # Calculate new values based on baseline + offset
        # Note: This assumes units match (e.g. % + %). 
        # If baseline is Hz and offset is Hz, it works. 
        # Mixing units is complex, but this simple addition works for standard use cases.
        
        new_rate = apply_offset(args.rate, rate_off)
        new_pitch = apply_offset(args.pitch, pitch_off)
        new_vol = apply_offset(args.volume, vol_off)

        variations[name] = {
            "Rate": new_rate,
            "Pitch": new_pitch,
            "Volume": new_vol,
            "Style": style,
            "Image": ""
        }

    # 5. Construct Character Object
    new_character = {
        "ReferenceID": next_id,
        "Alias": args.alias,
        "Engine": args.engine,
        "VoiceID": int(args.voice_id),
        "ShortName": voice_data["ShortName"],
        "Gender": voice_data["Gender"],
        "Locale": voice_data["Locale"],
        "Description": args.description,
        "SampleText": args.sample_text,
        "Baseline": {
            "Rate": args.rate,
            "Pitch": args.pitch,
            "Volume": args.volume
        },
        "Variations": variations
    }

    # 6. Save
    # Check if alias already exists and update it, or append new
    existing_index = next((i for i, c in enumerate(library) if c["Alias"] == args.alias), -1)
    
    if existing_index >= 0:
        print(f"Updating existing character: {args.alias}")
        # Preserve ID if updating
        new_character["ReferenceID"] = library[existing_index]["ReferenceID"]
        library[existing_index] = new_character
    else:
        print(f"Adding new character: {args.alias} (ID: {next_id})")
        library.append(new_character)

    with open(LIBRARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(library, f, indent=4)

    print(f"Character saved to {LIBRARY_FILE}")

if __name__ == "__main__":
    main()
