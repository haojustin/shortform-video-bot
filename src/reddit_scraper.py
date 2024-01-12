from bs4 import BeautifulSoup 
from selenium import webdriver 
import os, json, sys
sys.path.append('../src')
from scraper_utils import grammar_check, scroll_down, replace_profanity, add_data, get_data

# Create directory to save story data
save_directory = os.path.join("..", "data", "scraped_stories")
os.makedirs(save_directory, exist_ok=True)

# The urls to be scraped from
urls = [
    "https://www.reddit.com/r/AmItheAsshole/top/", 
    "https://www.reddit.com/r/stories/top/"
]
  
for url in urls:
    # Keep track of number of time we need to scroll the page
    count = 0
    # Whether or not a story is found in the url
    success = False

    while not success:
        # Initiating the webdriver 
        driver = webdriver.Chrome()  
        driver.get(url)
        
        # Ensures that the page dynamically loads more content
        scroll_down(driver, count)
        
        # Renders the JS code and stores all of the information in static HTML code
        html = driver.page_source 
        
        # Apply bs4 to html variable 
        soup = BeautifulSoup(html, "html.parser") 
        items = soup.find_all("shreddit-post")

        # Parse and store all titles and posts
        for item in items:
            post = ""
            paragraphs = item.find_all("p")
            for paragraph in paragraphs:
                post += paragraph.get_text()

            title = item.find_all("a", slot="title")
            title_text = title[0].get_text().strip()
            title_text = replace_profanity(title_text)

            used_stories = get_data("used_stories.txt")

            if len(post) != 0 and title_text not in used_stories:
                success = True

                # Apply grammar check (will be charged if >500 requests per month)
                # post = grammar_check(post)

                # Replace bad words
                post = replace_profanity(post)

                # Split story into parts (max 1 min per part)
                part = 1
                while len(post) > 0 and not post.isspace():
                    if part == 1:
                        post_start = post[:850]
                    split = 0

                    if len(post) > 900:
                        split = post.find(" ", 900)
                        story_data = {
                            "title": title_text + f" Part {part}",
                            "content": post[:split]
                        }
                        post = post[split:]
                    elif len(post) < 30:
                        story_data = {
                            "title": title_text + f" Part {part}",
                            "content": post + post_start
                        }
                        post = ""
                    else:
                        story_data = {
                            "title": title_text + f" Part {part}",
                            "content": post
                        }
                        post = ""

                    # Construct the file path for the JSON file to be saved
                    file_path = os.path.join(save_directory, f"story_{len(used_stories)+1}_part_{part}.json")

                    # Open the file in write mode and dump the story data as JSON
                    with open(file_path, "w", encoding="utf-8") as file:
                        json.dump(story_data, file, ensure_ascii=False, indent=4)

                    part += 1

                # Add current story to used stories
                add_data("used_stories.txt", title_text)

                break
        
        # Increment the number of times we need to scroll the page
        count += 1

driver.close()