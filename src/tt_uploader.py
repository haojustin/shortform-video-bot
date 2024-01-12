import os, json
from tiktok_uploader.upload import upload_videos
from tiktok_uploader.auth import AuthBackend

def tiktok_upload(filename, description):
    """
    Uploads videos with the given filename and description to TikTok.

    Parameters:
    filename - the filename of the video (string)
    description - the description of the video posted (string)
    """
    videos = [
        {
            'path': f"../data/captioned_videos/{filename}",
            'description': description
        }
    ]

    auth = AuthBackend(cookies="cookies.txt")
    failed_videos = upload_videos(videos=videos, auth=auth)

    for video in failed_videos:
        print(f'{video["path"]} with description "{video["description"]}" failed')


# Create path directories and list of data
videos_directory = os.path.join("..", "data", "captioned_videos")
videos_list = os.listdir(videos_directory)

stories_directory = os.path.join("..", "data", "scraped_stories")
stories_list = sorted(os.listdir(stories_directory))

for i in range(len(stories_list)):
    story_path = os.path.join(stories_directory, stories_list[i])

    # Get title of story
    with open(story_path, 'r', encoding='utf-8') as file:
        story_data = json.load(file)
    title = story_data.get("title", "")

    # Upload video with title and tags as the description
    tiktok_upload(videos_list[i], title + " #reddit #redditstories #redditreadings #askreddit #storynarrations #storytime #redditstorytime #fyp")