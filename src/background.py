import subprocess
import os
from pytube import YouTube

def download_and_crop_video(video_url, output_path, filename):
    
    """
    Downloads a YouTube video to the specified output path with a given filename.

    Parameters:
    video_url (str): URL of the YouTube video to be downloaded.
    output_path (str): Directory where the video will be saved.
    filename (str): Name of the file to be saved.
    """
    try:
        yt = YouTube(video_url)

        # Filter streams to get the highest quality video stream available
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4', res='1080p').first()
        if not video_stream:
            print(f"No 1080p stream available for {filename}. Downloading highest resolution available instead.")
            video_stream = yt.streams.get_highest_resolution()

        # Download the video
        temp_filepath = video_stream.download(output_path=output_path, filename=f"{filename}_temp")
        print(f"Completed download for {filename}")

        # Cropping and removing audio using FFmpeg
        # Crop to 9:16 aspect ratio (e.g., 1080x1920 resolution)
        final_filepath = os.path.join(output_path, f"{filename}.mp4")
        subprocess.run(['ffmpeg', '-i', temp_filepath, '-vf', 'crop=ih*9/16:ih', '-an', final_filepath], check=True)

        # Delete the original downloaded file with audio
        os.remove(temp_filepath)

    except Exception as e:
        print(f"Error processing video: {e}")

# Dictionary of video names and their corresponding YouTube links
video_dict = {
    'MC': 'https://www.youtube.com/watch?v=u7kdVe8q5zs'
}

output_directory = '../data/background'

for title, url in video_dict.items():
    download_and_crop_video(url, output_directory, title)
