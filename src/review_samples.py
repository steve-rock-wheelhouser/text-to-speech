#!/usr/bin/python3
# -*- coding: utf-8 -*-

# --- Script Summary ---
# Responsibility: Interactively review audio files in a directory. Plays files and sorts them into 'saved' or 'rejected' folders.
# Usage: python review_samples.py <directory> [--saved-folder SAVED] [--rejected-folder REJECTED]
# Examples:
#   python review_samples.py ./samples
#   python review_samples.py ./output --saved-folder keepers --rejected-folder trash
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

import os
import shutil
import sys
import args_utils

# Ensure we can import play_audio from the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from play_audio import play_audio
except ImportError:
    print("Error: play_audio.py not found. Please ensure it is in the same directory.")
    sys.exit(1)

def main():
    parser = args_utils.init_parser("Review audio samples: Play, Save, or Reject.")
    parser.add_argument("directory", help="Directory containing audio files to review")
    parser.add_argument("--saved-folder", default="saved", help="Name of the subfolder for saved files")
    parser.add_argument("--rejected-folder", default="rejected", help="Name of the subfolder for rejected files")
    args = parser.parse_args()

    source_dir = args.directory
    if not os.path.isdir(source_dir):
        print(f"Error: Directory '{source_dir}' does not exist.")
        sys.exit(1)

    # Define subdirectories
    saved_dir = os.path.join(source_dir, args.saved_folder)
    rejected_dir = os.path.join(source_dir, args.rejected_folder)

    # Create them if they don't exist
    os.makedirs(saved_dir, exist_ok=True)
    os.makedirs(rejected_dir, exist_ok=True)

    # Get list of audio files
    audio_extensions = ('.mp3', '.wav', '.ogg', '.m4a')
    files = [f for f in os.listdir(source_dir) 
             if f.lower().endswith(audio_extensions) and os.path.isfile(os.path.join(source_dir, f))]
    
    files.sort()

    if not files:
        print(f"No audio files found in '{source_dir}' to review.")
        return

    print(f"Found {len(files)} files. Starting review...")
    print("Controls: (s)ave, (r)eject, (p)lay-again, (q)uit")

    for filename in files:
        filepath = os.path.join(source_dir, filename)
        
        while True:
            print(f"\nFile: {filename}")
            play_audio(filepath)

            choice = input("Action [(s)ave, (r)eject, (p)lay-again, (q)uit]: ").lower().strip()

            if choice == 's':
                shutil.move(filepath, os.path.join(saved_dir, filename))
                print(" -> Saved.")
                break
            elif choice == 'r':
                shutil.move(filepath, os.path.join(rejected_dir, filename))
                print(" -> Rejected.")
                break
            elif choice == 'p':
                continue
            elif choice == 'q':
                print("Exiting review.")
                sys.exit(0)
            else:
                print("Invalid option.")

    print("\nAll files reviewed!")

if __name__ == "__main__":
    main()
