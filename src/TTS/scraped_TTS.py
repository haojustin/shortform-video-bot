from gtts import gTTS #google TTS
from pydub import AudioSegment #Custom TTS speed
import json
import os

# Define paths
stories_directory = os.path.join("..", "..", "data", "scraped_stories")
output_directory = os.path.join("..", "..", "data", "scraped_audio")
os.makedirs(output_directory, exist_ok=True)

# Process each story
for story_file in os.listdir(stories_directory):

    print(f"Processing file: {story_file}")

    if story_file.endswith('.json'):
        story_path = os.path.join(stories_directory, story_file)
        
        # Read story
        # Opens and reads the JSON file, extracting the story's title and content
        with open(story_path, 'r', encoding='utf-8') as file:
            story_data = json.load(file)
        title = story_data.get("title", "")
        content = story_data.get("content", "")

        # Concatenate title and content with a pause in between
        full_text = title + "\n\n" + content

        # Convert text to speech, create temp to further process audio
        tts = gTTS(full_text, lang='en')
        temp_path = os.path.join(output_directory, "temp.mp3")
        tts.save(temp_path)

        # Speed up the speech
        audio = AudioSegment.from_mp3(temp_path)
        faster_audio = audio.speedup(playback_speed=1.2)

        # Create a unique output filename for each story
        output_filename = f"{os.path.splitext(story_file)[0]}_audio.mp3"
        output_path = os.path.join(output_directory, output_filename)
        faster_audio.export(output_path, format="mp3")

        # Clean up temp
        os.remove(temp_path)

        print(f"TTS conversion completed, saved to: {output_path}")

print("All converted to TTS.")

