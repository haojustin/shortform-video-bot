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


def remove_story_data(directory, type, filename):
    """
    Removes the file specified by the directory, filename, and type given.

    Parameters:
    directory - path to the directory the file is in (string)
    type - ".mp4", ".png", ".mp3", ".json", or ".txt" (string)
    filename - the name of the file to be removed (string)
    """
    file_to_remove = os.path.join(directory, filename + type)
    os.remove(file_to_remove)


# Create path directories and list of data
videos_dir = os.path.join("..", "data", "captioned_videos")
videos_list = sorted(os.listdir(videos_dir))
print(videos_list)

raw_stories_dir = os.path.join("..", "data", "scraped_stories_raw")
stories_list = sorted(os.listdir(raw_stories_dir))
print(stories_list)

for i in range(len(stories_list)):
    story_path = os.path.join(raw_stories_dir, stories_list[i])

    # Get title of story
    with open(story_path, 'r', encoding='utf-8') as file:
        story_data = json.load(file)
    title = story_data.get("title", "")

    # Upload video with title and tags as the description
    tiktok_upload(videos_list[i], title + " #reddit #redditstories #redditreadings #storytime #askreddit #fyp #viral")

    # Delete used files
    filename = f"story_{stories_list[i][6]}_part_{stories_list[i][13]}"

    banner_dir = os.path.join("..", "data", "banner_complete")
    remove_story_data(banner_dir, ".png", filename)

    captioned_dir = os.path.join("..", "data", "captioned_videos")
    remove_story_data(captioned_dir, ".mp4", filename)

    combined_dir = os.path.join("..", "data", "combined_videos")
    remove_story_data(combined_dir, ".mp4", filename)

    audio_dir = os.path.join("..", "data", "scraped_audio")
    remove_story_data(audio_dir, ".mp3", filename)
    
    remove_story_data(raw_stories_dir, ".json", filename)

    stories_dir = os.path.join("..", "data", "scraped_stories")
    remove_story_data(stories_dir, ".json", filename)

    transcript_dir = os.path.join("..", "data", "transcripts")
    remove_story_data(transcript_dir, ".txt", filename)