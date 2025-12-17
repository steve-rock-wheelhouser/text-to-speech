# --- generate_speech_edge.py ---
# Start with setting the pitch and speed of the voice
python src/generate_speech_edge.py "Always with you, what can't be done" output.mp3 --voice en-US-GuyNeural --pitch="-10Hz" --rate="-35%" --play

# --- batch_generate.py ---
# Build the set of voices (male or female)
python src/batch_generate.py Male "Always with you what can't be done..." ./always-with-you-what-cant-be-done --pitch="-10Hz" --rate="-35%"

# --- review_samples.py ---
# Filter out the ones that you want using review_samples.py. Be sure to reference the source voice ID.
python src/review_samples.py ./always-with-you-what-cant-be-done

# --- save_character.py ---
# Create the baseline character in the voice-library/characters.json.
python src/save_character.py --alias "Yoda" --voice-id 210 --settings voice-library/always-with-you-what-cant-be-done/settings.json

# --- character_lines.py ---
# Create new audio files for the character.
python src/character_lines.py --alias "Yoda" --variation "Calm" --lines "Always with you what can't be done..." --output-dir voice-library/characters/Yoda --file-name "what_cant_be_done"

# Use these character audio files in your favorite apps!
test_sound.sh --file voice-library/characters/Yoda/Calm/what_cant_be_done.mp3

# --- play_audio.py ---
# python app
python src/play_audio.py --file voice-library/characters/Yoda/Calm/what_cant_be_done.mp3
