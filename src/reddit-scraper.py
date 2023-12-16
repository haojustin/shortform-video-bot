from bs4 import BeautifulSoup 
from selenium import webdriver 
import time

def scroll_down(driver, limit):
    """
    A function for scrolling the page.
     
    Parameters: 
    driver - an instance of WebDriver
    limit - specifies how many times to scroll and is a non-negative integer
    """
    for i in range(limit):
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

url = "https://www.reddit.com/r/AmItheAsshole/"
  
# Initiating the webdriver 
driver = webdriver.Chrome()  
driver.get(url)  
  
# Ensures that the page dynamically loads more content
scroll_down(driver, 3)
  
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
    posts.append(post)

    title = item.find_all("a", slot="title")
    titles.append(title[0].get_text())

# Print titles and corresponding posts
for i in range(len(posts)):
    print("START \n")
    print(titles[i])
    print(posts[i])
    print("\nEND \n")

driver.close()