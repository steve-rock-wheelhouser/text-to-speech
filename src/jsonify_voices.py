#!/usr/bin/python3
# --- Script Summary ---
# Responsibility: Reads voices.json and adds sequential IDs to each voice entry for easier referencing.
# Usage: python jsonify_voices.py
# Examples:
#   python jsonify_voices.py
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
# pip install json
#===============================================================================================================

import json
import os

FILE_PATH = "/home/user/projects/Text-to-Speech/voices.json"

def add_ids_to_voices():
    if not os.path.exists(FILE_PATH):
        print(f"File not found: {FILE_PATH}")
        return

    print(f"Reading {FILE_PATH}...")
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        try:
            voices = json.load(f)
        except json.JSONDecodeError:
            print("Error: voices.json is not valid JSON.")
            return

    # Add sequential IDs
    for i, voice in enumerate(voices, 1):
        voice["ID"] = i

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(voices, f, indent=4)
    
    print(f"Updated {len(voices)} voices with IDs in {FILE_PATH}")

if __name__ == "__main__":
    add_ids_to_voices()