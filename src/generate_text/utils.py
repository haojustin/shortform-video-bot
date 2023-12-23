import requests
import time
import os

def grammar_spell_check(text):
    """
    A function for fixing the grammar and spelling of the given text.
     
    Parameters: 
    text - the text to check (string)
    """
    RAPID_API_KEY = os.environ.get("RAPID_API_KEY")
    url = "https://textgears-textgears-v1.p.rapidapi.com/correct"

    payload = { "text": text }
    headers = {
		"content-type": "application/x-www-form-urlencoded",
		"X-RapidAPI-Key": RAPID_API_KEY,
		"X-RapidAPI-Host": "textgears-textgears-v1.p.rapidapi.com"
	}

    response = requests.post(url, data=payload, headers=headers)

    return response.json()["response"]["corrected"]

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