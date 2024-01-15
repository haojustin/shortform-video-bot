import requests, time, os, re

def grammar_check(text):
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


def replace_profanity(input_text):
    """ 
    Returns the input string with profanity replaced with the corresponding
    replacement word.

    Parameter:
    input_text - the text to filter through (string)
    """
    # Get list of profanity and their replacements
    profanity = get_data("profanity.txt")
    replacement_words = get_data("replacement_words.txt")

    # Replace the profanity in the text if it exists
    for i in range(len(profanity)):
        word = re.compile(re.escape(profanity[i]), re.IGNORECASE)
        input_text = word.sub(replacement_words[i], input_text)
    
    return input_text


def get_data(file):
    """ 
    Gets the word list from the provided file.

    Parameter:
    file - name of the file containing the words to be loaded (string)
         - should be a flat text file with one profanity entry per line
    """
    # Get path to data folder in src
    ROOT = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(ROOT, 'data', file)

    # Create list of words from the txt files
    f = open(filename)
    wordlist = f.readlines()
    wordlist = [w.strip() for w in wordlist if w]
    
    return wordlist

def add_data(file, data):
    """
    Adds a new line of data to the specified file.

    Parameters:
    file - name of the file to be modified (string)
    data - line to be added to the file (string)
    """
    # Get path to data folder in src
    ROOT = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(ROOT, 'data', file)

    # Add data to new line
    with open(filename, "a") as f:
        f.write(data + "\n")

def estimate_reading_time(text):
    words_per_second = 200 / 60  # 200 words per minute
    word_count = len(text.split())
    return word_count / words_per_second