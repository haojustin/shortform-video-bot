from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os
import re

def parse_transcript(transcript_file):
    """
    Parses the transcript file into a list of tuples with time stamps and text

    Parameters: 

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

base_dir = '..'
transcripts_dir = os.path.join(base_dir, 'data/transcripts')
videos_dir = os.path.join(base_dir, 'data/combined_videos')
output_dir = os.path.join(base_dir, 'data/captioned_videos')
os.makedirs(output_dir, exist_ok=True)

for video_file in os.listdir(videos_dir):
    if video_file.endswith('.mp4'):
        video_path = os.path.join(videos_dir, video_file)
        transcript_path = os.path.join(transcripts_dir, os.path.splitext(video_file)[0] + '.txt')
        output_video_path = os.path.join(output_dir, 'captioned_' + video_file)

        if os.path.exists(transcript_path):
            transcript = parse_transcript(transcript_path)
            generate_video_with_captions(video_path, transcript, output_video_path)
            print(f"Captioned video created: {output_video_path}")
        else:
            print(f"No transcript found for {video_file}")
