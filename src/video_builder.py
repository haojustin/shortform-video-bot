import os, re, json, textwrap, random
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ImageClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont

# PART 1 - COMBINE MP4 AND MP3
base_dir = ".."
audio_dir = os.path.join(base_dir, "data/scraped_audio")
video_dir = os.path.join(base_dir, "data/background")
output_dir = os.path.join(base_dir, "data/combined_videos")

def get_random_start_point(video_duration, audio_duration):
    """
    Returns a random start point for a video clip, ensuring the video is still long enough for the audio.
    """
    latest_valid_start = max(video_duration - audio_duration, 0)
    return random.uniform(0, latest_valid_start)

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Get a random video file
video_files = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]
if not video_files:
    raise Exception("No video files found in background directory.")
random_video_file = os.path.join(video_dir, random.choice(video_files))

# Process each audio file
for audio_file in os.listdir(audio_dir):
    if audio_file.endswith(".mp3"):
        audio_path = os.path.join(audio_dir, audio_file)
        audio_clip = AudioFileClip(audio_path)

        if audio_clip.duration <= 0:
            print(f"Error loading audio from {audio_file}")
            continue

        # Load the video
        base_video_clip = VideoFileClip(random_video_file)
        if base_video_clip.duration < audio_clip.duration:
            print(f"Video clip is shorter than audio clip for {audio_file}")
            base_video_clip.close()
            continue

        # Get a random start point for the video clip
        start_time = get_random_start_point(base_video_clip.duration, audio_clip.duration)
        video_clip = base_video_clip.subclip(start_time, start_time + audio_clip.duration)

        # Combine audio and video
        final_clip = video_clip.set_audio(audio_clip)

        # Output file path
        output_file = os.path.join(output_dir, f"{audio_file.split('.')[0]}.mp4")

        # Write the result to a file in 1080p resolution
        final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac", bitrate="8000k", fps=30)

        print(f"Created {output_file}")

        # Close the clips to free resources
        base_video_clip.close()
        final_clip.close()

def add_title_to_banner(story_json_path, banner_template_path, output_banner_path):
    with open(story_json_path, "r", encoding="utf-8") as file:
        story_data = json.load(file)
    
    title_text = story_data["title"]
    
    image = Image.open(banner_template_path)
    font = ImageFont.truetype('../data/font/h.otf', 13)
    draw = ImageDraw.Draw(image)

    # Coordinates for text placement
    text_x, text_y = 450, 340
    
    # Hardcoded character limit per line - adjust as needed
    max_chars_per_line = 47  # Change this number based on your specific requirements

    # Wrap text
    wrapped_text = textwrap.wrap(title_text, width=max_chars_per_line)

    # Manually calculate the height of each line based on font size
    line_height = font.size + 5 

    # Draw each line of text
    for line in wrapped_text:
        draw.text((text_x, text_y), line, font=font, fill="black")
        text_y += line_height  # Increment y-coordinate by line height

    # Save the banner
    if not os.path.exists(os.path.dirname(output_banner_path)):
        os.makedirs(os.path.dirname(output_banner_path))
    
    image.save(output_banner_path)

story_json_dir = os.path.join(base_dir, "data/scraped_stories_raw")
banner_template_dir = os.path.join(base_dir, "data/banner_template")
banner_complete_dir = os.path.join(base_dir, "data/banner_complete")
os.makedirs(banner_complete_dir, exist_ok=True)

story_json_files = os.listdir(story_json_dir)
banner_template_files = os.listdir(banner_template_dir)

if story_json_files and banner_template_files:
    banner_template_path = os.path.join(banner_template_dir, banner_template_files[0])  

    for story_json_file in story_json_files:
        story_json_path = os.path.join(story_json_dir, story_json_file)
        output_banner_path = os.path.join(banner_complete_dir, f"{os.path.splitext(story_json_file)[0]}.png")

        # Call the function with the paths
        add_title_to_banner(story_json_path, banner_template_path, output_banner_path)
        print(f"Banner with title created at: {output_banner_path}")
else:
    print("Required files are missing.")

# PART 2 - ADD CAPTIONS TO COMBINED VIDEO
        
def parse_transcript(transcript_file):
    """
    Parses the transcript file into a list of tuples with time stamps and text

    Parameter: 
    transcript_file - the path to the transcript file (string)
    """
    with open(transcript_file, 'r') as file:
        content = file.read()

    pattern = r"\((\d+\.\d+), (\d+\.\d+)\): (.+)"
    matches = re.findall(pattern, content)
    return [(float(start), float(end), text) for start, end, text in matches]


def generate_video_with_captions(video_path, transcript, banner_path, output_path):
    """
    Overlays the video with captions

    Parameters: 
    video_path - path to video that needs to be captioned (string)
    transcript - time stamps and caption text (list of tuples)
    output_path - path to where the final video is stored (string)
    """
    video_clip = VideoFileClip(video_path)

    # Load the banner as an image clip and set its duration
    banner_duration = next((end for start, end, text in transcript if "part" in text.lower()), video_clip.duration)
    banner_clip = ImageClip(banner_path).set_duration(banner_duration).set_position('center')

    subtitle_clips = []
    for start, end, text in transcript:
        subtitle_clip = TextClip(text, fontsize=40, color='white', font='Impact',
                                 stroke_color='black', stroke_width=2)
        subtitle_clip = subtitle_clip.set_pos('center').set_duration(end - start).set_start(start)
        subtitle_clips.append(subtitle_clip)

    # Create the final clip. Add the banner last to ensure it's on top
    final_clip = CompositeVideoClip([video_clip] + subtitle_clips + [banner_clip], size=video_clip.size)
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    video_clip.close()
    final_clip.close()


transcripts_dir = os.path.join(base_dir, 'data/transcripts')
videos_dir = os.path.join(base_dir, 'data/combined_videos')
output_dir = os.path.join(base_dir, 'data/captioned_videos')

os.makedirs(output_dir, exist_ok=True)

for video_file in os.listdir(videos_dir):

    if video_file.endswith('.mp4'):

        video_path = os.path.join(videos_dir, video_file)
        transcript_path = os.path.join(transcripts_dir, os.path.splitext(video_file)[0] + '.txt')
        output_video_path = os.path.join(output_dir, 'captioned_' + video_file)

        banner_path = os.path.join(banner_complete_dir, os.path.splitext(video_file)[0] + '.png')  
        
        if os.path.exists(transcript_path):
            transcript = parse_transcript(transcript_path)
            generate_video_with_captions(video_path, transcript, banner_path, output_video_path)
            print(f"Captioned video created: {output_video_path}")
        else:
            print(f"No transcript found for {video_file}")
