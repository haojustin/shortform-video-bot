import os, re
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

# PART 1 - COMBINE MP4 AND MP3

base_dir = ".." 
audio_dir = os.path.join(base_dir, "data/scraped_audio")
video_dir = os.path.join(base_dir, "data/background")
output_dir = os.path.join(base_dir, "data/combined_videos")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Get video file
video_files = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]
if not video_files:
    raise Exception("No video files found in background directory.")
video_file = os.path.join(video_dir, video_files[0])

# Load the video
base_video_clip = VideoFileClip(video_file)

# Process each audio file
for audio_file in os.listdir(audio_dir):
    if audio_file.endswith(".mp3"):
        audio_path = os.path.join(audio_dir, audio_file)
        audio_clip = AudioFileClip(audio_path)

        # Check if audio is loaded correctly
        if audio_clip.duration <= 0:
            print(f"Error loadng audio from {audio_file}")
            continue

        # Loop video to match audio length
        loops = int(audio_clip.duration // base_video_clip.duration) + 1
        video_clip = concatenate_videoclips([base_video_clip] * loops)
        video_clip = video_clip.subclip(0, audio_clip.duration)

        # Combine audio and video
        final_clip = video_clip.set_audio(audio_clip)

        # Output file path
        output_file = os.path.join(output_dir, f"{audio_file.split('.')[0]}.mp4")

        # Write the result to a file
        final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

        print(f"Created {output_file}")


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


def generate_video_with_captions(video_path, transcript, output_path):
    """
    Overlays the video with captions

    Parameters: 
    video_path - path to video that needs to be captioned (string)
    transcript - time stamps and caption text (list of tuples)
    output_path - path to where the final video is stored (string)
    """
    video_clip = VideoFileClip(video_path)

    subtitle_clips = []
    for start, end, text in transcript:
        subtitle_clip = TextClip(text, fontsize=50, color='white', font='Impact',
                                 stroke_color='purple', stroke_width=2)
        subtitle_clip = subtitle_clip.set_pos('center').set_duration(end - start).set_start(start)
        subtitle_clips.append(subtitle_clip)

    final_clip = CompositeVideoClip([video_clip] + subtitle_clips)
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    video_clip.close()
    final_clip.close()


# Create directory paths
transcripts_dir = os.path.join(base_dir, 'data/transcripts')
videos_dir = os.path.join(base_dir, 'data/combined_videos')
output_dir = os.path.join(base_dir, 'data/captioned_videos')

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

for video_file in os.listdir(videos_dir):
    # Check if the video file is an mp4 file
    if video_file.endswith('.mp4'):
        # Create file paths
        video_path = os.path.join(videos_dir, video_file)
        transcript_path = os.path.join(transcripts_dir, os.path.splitext(video_file)[0] + '.txt')
        output_video_path = os.path.join(output_dir, 'captioned_' + video_file)

        # Check if there exists a transcript for the video
        if os.path.exists(transcript_path):
            # Transform transcript into list of (start time, end time, text)
            transcript = parse_transcript(transcript_path)
            # Add text to video
            generate_video_with_captions(video_path, transcript, output_video_path)
            print(f"Captioned video created: {output_video_path}")
        else:
            print(f"No transcript found for {video_file}")
