from boto3 import Session
from contextlib import closing
import os
import json

def convert_tts(title, content, output_path):
    session = Session() 
    polly = session.client("polly")

    try:
        full_text = title + "\n\n" + content
        response = polly.synthesize_speech(Engine="neural", Text=full_text, OutputFormat="mp3", VoiceId="Joanna")

        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                try:
                    with open(output_path, "wb") as file:
                        file.write(stream.read())
                    print(f"audio file saved: {output_path}")
                except IOError as error:
                    print(f"failed to write to file: {error}")
        else:
            print("cant stream audio")

    except Exception as e:
        print(f" error during TTS: {e}")

base_dir = ".."
stories_dir = os.path.join(base_dir, "data/scraped_stories")
audio_dir = os.path.join(base_dir, "data/scraped_audio")
os.makedirs(audio_dir, exist_ok=True)

for story_file in os.listdir(stories_dir):
    if story_file.endswith('.json'):
        story_path = os.path.join(stories_dir, story_file)
        with open(story_path, 'r', encoding='utf-8') as file:
            story_data = json.load(file)
        title = story_data.get("title", "")
        content = story_data.get("content", "")

        output_filename = os.path.splitext(story_file)[0] + '.mp3'
        output_path = os.path.join(audio_dir, output_filename)
        convert_tts(title, content, output_path)
