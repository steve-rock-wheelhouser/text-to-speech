#!/usr/bin/python3
# -*- coding: utf-8 -*-


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
# pip install args_utils
# pip install edge-tts
# pip install pygame
# pip install ffmpeg-python
# pip install pydub
# pip install mutagen
#===============================================================================================================


import argparse
import json
import os
import subprocess
import sys

# Path to the characters database
CHARACTERS_FILE = "/home/user/projects/Text-to-Speech/voice-library/characters.json"

def load_character(alias):
    """Loads character details from the JSON library."""
    if not os.path.exists(CHARACTERS_FILE):
        print(f"Error: {CHARACTERS_FILE} not found. Please run save_character.py first.")
        sys.exit(1)

    with open(CHARACTERS_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Failed to decode {CHARACTERS_FILE}.")
            sys.exit(1)

    # characters.json is a list of objects
    for char in data:
        if char.get("Alias") == alias:
            return char
            
    print(f"Error: Character '{alias}' not found in {CHARACTERS_FILE}.")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Generate audio lines for a character.")
    parser.add_argument("--alias", required=True, help="Character alias (e.g., Yoda)")
    parser.add_argument("--variation", required=True, help="Variation folder (e.g., Calm)")
    parser.add_argument("--lines", required=True, help="Text content to generate")
    parser.add_argument("--output-dir", required=True, help="Base output directory")
    parser.add_argument("--file-name", required=True, help="Output filename (without extension)")

    args = parser.parse_args()

    # Load character settings
    character = load_character(args.alias)
    
    # Resolve Voice (ShortName is the edge-tts ID)
    voice = character.get("ShortName")
    if not voice:
        print(f"Error: No voice ShortName found for character '{args.alias}'.")
        sys.exit(1)

    # Resolve Variation Settings
    variations = character.get("Variations", {})
    if args.variation not in variations:
        print(f"Error: Variation '{args.variation}' not found for character '{args.alias}'.")
        print(f"Available variations: {', '.join(variations.keys())}")
        sys.exit(1)

    var_settings = variations[args.variation]
    pitch = var_settings.get("Pitch", "+0Hz")
    rate = var_settings.get("Rate", "+0%")

    # Prepare output paths
    full_output_dir = os.path.join(args.output_dir, args.variation)
    os.makedirs(full_output_dir, exist_ok=True)
    output_file = os.path.join(full_output_dir, f"{args.file_name}.mp3")

    # Call the generation script
    # Use absolute path to sibling script to ensure it works from any CWD
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gen_script = os.path.join(script_dir, "generate_speech_edge.py")
    
    cmd = [sys.executable, gen_script, args.lines, output_file, "--voice", voice, "--pitch", pitch, "--rate", rate]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()
