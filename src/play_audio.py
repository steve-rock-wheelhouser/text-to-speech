#!/usr/bin/python3
# -*- coding: utf-8 -*-

# --- Script Summary ---
# Responsibility: Robust audio player that tries Pygame, system CLI players, and Flatpak host spawning.
# Usage: python play_audio.py <file>
# Examples:
#   python play_audio.py output.mp3
#   python play_audio.py /path/to/audio.wav
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
import sys
import time
import subprocess
import shutil
import args_utils

def play_audio(file_path):
    file_path = os.path.abspath(file_path)
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    print(f"Playing: {file_path}")

    # 1. Try Pygame (Best Python-native option)
    # Requires: pip install pygame
    try:
        import pygame
        # Suppress pygame welcome message
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        # Keep script running while music plays
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        return
    except ImportError:
        pass # Pygame not installed, try fallbacks
    except Exception as e:
        print(f"Pygame playback failed: {e}")

    # 2. Try System Players (Linux/macOS fallback)
    # paplay = PulseAudio (Standard on Fedora/Ubuntu)
    # aplay = ALSA (Linux)
    # afplay = macOS
    # ffplay = FFmpeg
    players = [
        ("paplay", []),
        ("mpg123", []),
        ("afplay", []),
        ("aplay", []),
        ("ffplay", ["-nodisp", "-autoexit", "-hide_banner"]),
    ]

    for player_cmd, args in players:
        if shutil.which(player_cmd):
            try:
                subprocess.run([player_cmd] + args + [file_path], check=True)
                return
            except subprocess.CalledProcessError:
                continue

    # 3. Flatpak Fallback (For VS Code sandbox)
    if shutil.which("flatpak-spawn"):
        print("Detecting Flatpak environment. Attempting to play on host...")
        try:
            subprocess.run(["flatpak-spawn", "--host", "paplay", file_path], check=True)
            return
        except subprocess.CalledProcessError:
            print("Failed to play via flatpak-spawn.")

    print("Error: Could not play audio. Please install 'pygame' (pip install pygame).")
    sys.exit(1)

if __name__ == "__main__":
    parser = args_utils.init_parser("Simple Audio Player")
    parser.add_argument("file", help="Path to the audio file to play")
    args = parser.parse_args()

    play_audio(args.file)
