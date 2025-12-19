#!/usr/bin/python3
# -*- coding: utf-8 -*-

# --- Script Summary ---
# Responsibility: Batch generate audio samples for all voices of a specific gender from voices.json.
# Usage: python batch_generate.py <Male|Female> <text> <output_dir> [--pitch PITCH] [--rate RATE]
# Examples:
#   python batch_generate.py Male "Always with you what can't be done..." ./always-with-you-what-cant-be-done --pitch="-10Hz" --rate="-35%"
#   python batch_generate.py Female "Testing speed" ./female_fast --rate="+20%"
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
# pip install args_utils
#===============================================================================================================

import json
import subprocess
import os
import sys
import args_utils

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VOICES_FILE = os.path.join(SCRIPT_DIR, "voices.json")
SAMPLE_SCRIPT = os.path.join(SCRIPT_DIR, "sample_voices.py")

def main():
    parser = args_utils.init_parser("Batch generate samples for a specific gender.")
    parser.add_argument("gender", choices=["Male", "Female"], help="Gender to filter by")
    args_utils.add_text_arg(parser)
    parser.add_argument("output_dir", help="Directory to save output")
    args_utils.add_pitch_rate_args(parser)
    
    args = parser.parse_args()

    if not os.path.exists(VOICES_FILE):
        print(f"Error: {VOICES_FILE} not found.")
        sys.exit(1)

    if not os.path.exists(SAMPLE_SCRIPT):
        print(f"Error: {SAMPLE_SCRIPT} not found.")
        sys.exit(1)

    print(f"Reading voices from {VOICES_FILE}...")
    with open(VOICES_FILE, 'r', encoding='utf-8') as f:
        voices = json.load(f)

    # Filter IDs based on Gender
    ids = [str(v['ID']) for v in voices if v.get('Gender') == args.gender and 'ID' in v]
    
    if not ids:
        print(f"No voices found for gender: {args.gender}")
        return

    print(f"Found {len(ids)} {args.gender} voices.")
    
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Save generation settings for reproducibility
    settings = {
        "pitch": args.pitch,
        "rate": args.rate,
        "gender": args.gender,
        "text": args.text
    }
    with open(os.path.join(args.output_dir, "settings.json"), "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)

    # Construct command to call sample_voices.py
    id_list = ",".join(ids)
    
    cmd = [
        sys.executable, SAMPLE_SCRIPT,
        args.text,
        id_list,
        f"--pitch={args.pitch}",
        f"--rate={args.rate}",
        "--output-dir", args.output_dir
    ]
    
    print(f"Running batch generation for {args.gender} voices into '{args.output_dir}'...")
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
