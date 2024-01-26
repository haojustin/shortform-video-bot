import os, json
from boto3 import Session
from contextlib import closing

import os, json
from boto3 import Session
from contextlib import closing

def convert_tts(title, content, output_path, speech_rate="120%"):
    """
    Creates an mp3 audio file from the given story title and content with adjustable speech rate.

    Parameters:
    title - the story title (string)
    content - the story content (string)
    output_path - path of where to store the audio file (string)
    speech_rate - speed of the speech as a percentage (string, default "100%")
    """
    session = Session() 
    polly = session.client("polly")

    # Adjust speech rate using SSML
    ssml_text = f"<speak><prosody rate='{speech_rate}'>{title}</prosody>\n\n\n\n<prosody rate='{speech_rate}'>{content}</prosody></speak>"

    try:
        response = polly.synthesize_speech(Engine="neural", Text=ssml_text, TextType="ssml", OutputFormat="mp3", VoiceId="Joanna")

        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                try:
                    with open(output_path, "wb") as file:
                        file.write(stream.read())
                    print(f"Audio file saved: {output_path}")
                except IOError as error:
                    print(f"Failed to write to file: {error}")
        else:
            print("Cannot stream audio")

    except Exception as e:
        print(f"Error during TTS: {e}")


# Create directory paths
base_dir = ".."
stories_dir = os.path.join(base_dir, "data/scraped_stories")
audio_dir = os.path.join(base_dir, "data/scraped_audio")

# Ensure audio directory exists
os.makedirs(audio_dir, exist_ok=True)

for story_file in os.listdir(stories_dir):
    # Check if the story file is a json file
    if story_file.endswith('.json'):
        story_path = os.path.join(stories_dir, story_file)

        # Get story data
        with open(story_path, 'r', encoding='utf-8') as file:
            story_data = json.load(file)
        title = story_data.get("title", "")
        content = story_data.get("content", "")

        # Create audio file name and path
        output_filename = os.path.splitext(story_file)[0] + '.mp3'
        output_path = os.path.join(audio_dir, output_filename)

        # Create and store audio file
        convert_tts(title, content, output_path)
