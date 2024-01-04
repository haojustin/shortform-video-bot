import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

base_dir = ".." 
audio_dir = os.path.join(base_dir, "data/scraped_audio")
video_dir = os.path.join(base_dir, "data/videos")
output_dir = os.path.join(base_dir, "data/combined_videos")

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get video file
video_files = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]
if not video_files:
    raise Exception("No video files found in videos directory.")
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
        output_file = os.path.join(output_dir, f"combined_{audio_file.split('.')[0]}.mp4")

        # Write the result to a file
        final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

        print(f"Created {output_file}")
