import requests

def grammar_spell_check(text):
	"""
    A function for fixing the grammar and spelling of the given text.
     
    Parameters: 
    text - the text to check (string)
    """
	url = "https://textgears-textgears-v1.p.rapidapi.com/correct"

	payload = { "text": text }
	headers = {
		"content-type": "application/x-www-form-urlencoded",
		"X-RapidAPI-Key": "e645dfa1cbmshe5101813d57d786p174249jsn17471126608c",
		"X-RapidAPI-Host": "textgears-textgears-v1.p.rapidapi.com"
	}

	response = requests.post(url, data=payload, headers=headers)

	return response.json()["response"]["corrected"]