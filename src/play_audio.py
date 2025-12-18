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
import signal
import args_utils

child_process = None

def signal_handler(sig, frame):
    """Gracefully terminate the child process or pygame."""
    global child_process
    if child_process and child_process.poll() is None:
        child_process.terminate()
    
    try:
        import pygame
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
    except (ImportError, pygame.error):
        pass
    
    sys.exit(0)

# Register the signal handler for termination signals
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

def play_audio(file_path):
    global child_process
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
                child_process = subprocess.Popen([player_cmd] + args + [file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                child_process.wait()
                return
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue

    # 3. Flatpak Fallback (For VS Code sandbox)
    if shutil.which("flatpak-spawn"):
        print("Detecting Flatpak environment. Attempting to play on host...")
        try:
            child_process = subprocess.Popen(["flatpak-spawn", "--host", "paplay", file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            child_process.wait()
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Failed to play via flatpak-spawn.")

    print("Error: Could not play audio. Please install 'pygame' (pip install pygame).")
    sys.exit(1)

if __name__ == "__main__":
    parser = args_utils.init_parser("Simple Audio Player")
    parser.add_argument("file", help="Path to the audio file to play")
    args = parser.parse_args()

    play_audio(args.file)
