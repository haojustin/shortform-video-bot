import subprocess

def run():
    """
    Runs the entire application.
    """
    subprocess.run("python reddit_scraper.py", shell=True)
    subprocess.run("python tts_converter.py", shell=True)
    subprocess.run("python transcript_creator.py", shell=True)
    subprocess.run("python video_builder.py", shell=True)
    subprocess.run("python tiktok_upload.py", shell=True)

if __name__ == "__main__":
    run()