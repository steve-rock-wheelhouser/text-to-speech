#!/bin/bash

echo "Diagnosing sound capability..."

# 1. Try PulseAudio (paplay) - Common on desktop Linux
if command -v paplay &> /dev/null; then
    echo "Found: paplay"
    # Try specific sound, then fallback to finding any sound
    SOUND="/usr/share/sounds/freedesktop/stereo/complete.oga"
    if [ ! -f "$SOUND" ]; then
        SOUND=$(find /usr/share/sounds -type f \( -name "*.oga" -o -name "*.wav" -o -name "*.ogg" \) 2>/dev/null | head -n 1)
    fi

    # If still no sound, generate one with Python
    if [ -z "$SOUND" ] && command -v python3 &> /dev/null; then
        echo "No system sounds found. Generating beep.wav..."
        python3 -c "import wave, struct, math; w=wave.open('/tmp/beep.wav','w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100); d=b''.join([struct.pack('<h', int(32767.0*math.sin(440.0*math.pi*2*i/44100))) for i in range(22050)]); w.writeframes(d); w.close()"
        SOUND="/tmp/beep.wav"
    fi

    if [ -n "$SOUND" ] && [ -f "$SOUND" ]; then
        echo "Playing $SOUND with paplay"
        paplay "$SOUND"
        exit 0
    else
        echo "Warning: paplay found but no sound files found or generated."
    fi
else
    echo "Missing: paplay"
fi

# 2. Try ALSA (aplay)
if command -v aplay &> /dev/null; then
    echo "Found: aplay"
    SOUND="/usr/share/sounds/alsa/Front_Center.wav"
    if [ ! -f "$SOUND" ]; then
        SOUND=$(find /usr/share/sounds -name "*.wav" 2>/dev/null | head -n 1)
    fi

    if [ -n "$SOUND" ] && [ -f "$SOUND" ]; then
        echo "Playing $SOUND with aplay"
        aplay "$SOUND"
        exit 0
    else
        echo "Warning: aplay found but no .wav sound files found."
    fi
else
    echo "Missing: aplay"
fi

# 3. Try speaker-test (ALSA synthetic tone) - No files required
if command -v speaker-test &> /dev/null; then
    echo "Found: speaker-test. Generating sine wave..."
    speaker-test -t sine -f 440 -l 1 >/dev/null 2>&1 && exit 0
    echo "speaker-test failed (no audio device?)"
else
    echo "Missing: speaker-test"
fi

# 4. Fallback
echo "Fallback to system bell..."
echo -e "\a"