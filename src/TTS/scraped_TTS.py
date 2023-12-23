from gtts import gTTS # Google TTS
from pydub import AudioSegment # Custom Audio Adjustment
import json
import os

def convert_tts(title, content, output_path):
    """
    Convert the given title and content to speech and save to the specified output path
    The speech is sped up by a factor of 1.2

    Parameters:
    title - the title of the story (string)
    content - the story itself (string)
    output_path - the file path where the TTS audio will be saved (string)
    """

    # Pause after title
    full_text = title + "\n\n" + content

    # Convert text to speech, create temp to further process audio
    tts = gTTS(full_text, lang='en')
    temp_path = os.path.join(os.path.dirname(output_path), "temp.mp3")
    tts.save(temp_path)

    # Speed up the speech
    audio = AudioSegment.from_mp3(temp_path)
    # faster_audio = audio.speedup(playback_speed=1.2)

    # Save the processed audio
    # faster_audio.export(output_path, format="mp3")
    audio.export(output_path, format="mp3")

    # Clean up temporary file
    os.remove(temp_path)

# Define paths
stories_directory = os.path.join("..", "..", "data", "scraped_stories")
output_directory = os.path.join("..", "..", "data", "scraped_audio")
os.makedirs(output_directory, exist_ok=True)

# Print titles and corresponding posts into data/scraped_stories
for story_file in os.listdir(stories_directory):
    print(f"Processing file: {story_file}")

    if story_file.endswith('.json'):
        story_path = os.path.join(stories_directory, story_file)
        
        # Read story
        with open(story_path, 'r', encoding='utf-8') as file:
            story_data = json.load(file)
        title = story_data.get("title", "")
        content = story_data.get("content", "")

        # Create a unique output filename for each story
        output_filename = f"{os.path.splitext(story_file)[0]}_audio.mp3"

        # Construct the file path for the JSON file to be saved
        output_path = os.path.join(output_directory, output_filename)

        # Convert and save the story as TTS
        convert_tts(title, content, output_path)

        print(f"TTS conversion completed, saved to: {output_path}")

print("All stories have been converted to TTS.")
