from bs4 import BeautifulSoup 
from selenium import webdriver 
import os
import json
import sys
sys.path.append('../../src')
from utils import grammar_spell_check, scroll_down, replace_bad_words

save_directory = os.path.join("..", "..", "data", "scraped_stories")
os.makedirs(save_directory, exist_ok=True)

url = "https://www.reddit.com/r/AmItheAsshole/"
  
# Initiating the webdriver 
driver = webdriver.Chrome()  
driver.get(url)  
  
# Ensures that the page dynamically loads more content
scroll_down(driver, 1)
  
# Renders the JS code and stores all of the information in static HTML code
html = driver.page_source 
  
# Apply bs4 to html variable 
soup = BeautifulSoup(html, "html.parser") 
items = soup.find_all("shreddit-post")

# Parse and store all titles and posts
posts = []
titles = []
for item in items:
    post = ""
    paragraphs = item.find_all("p")
    for paragraph in paragraphs:   
        post += paragraph.get_text()
    # Apply grammar and spelling check (will be charged if >500 requests per month)
    # post = grammar_spell_check(post)
    # Replace bad words
    post = replace_bad_words(post)
    posts.append(post)

    title = item.find_all("a", slot="title")
    titles.append(title[0].get_text())

# Print titles and corresponding posts into data/scraped_stories
for i, (title, post) in enumerate(zip(titles, posts)):

    story_data = {
        "title": title,
        "content": post
    }

    # Construct the file path for the JSON file to be saved
    file_path = os.path.join(save_directory, f"story_{i}.json")

    # Open the file in write mode and dump the story data as JSON
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(story_data, file, ensure_ascii=False, indent=4)


driver.close()