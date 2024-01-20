# Short-Form Video Bot

This bot 
- web-scrapes interesting stories from Reddit using **Selenium** and **Beautiful Soup**
- creates a mp3 audio file of the story using **AWS Polly**
- creates a transcript of the audio file using **Google Cloud Speech to Text**
- combines a mp4 video with the mp3 audio and adds the subtitles to the combined video using **MoviePy**
- automatically posts to @reddit_story_narrator on TikTok with **tiktok-uploader**

The `main.py` script will automatically run every 2 hours with **AWS Lambda** and **Amazon CloudWatch**. Uploading to more platforms is also in the works.