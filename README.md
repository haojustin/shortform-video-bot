# TTS-Caption-Bot

Make sure to have Python3 installed, or replace all uses of python with python3.
1. Create a virtual environment with `python -m venv venv`
2. Activate the virtual environment with `. venv/bin/activate`
3. Install requirements with `pip install requirements.txt`
4. Install ffmpeg with `brew install ffmpeg`
5. Create a .envrc file with the provided template
6. Run the scraper with `python reddit_scraper.py` (make sure you are in the correct directory)
7. Run the TTS with `python scraped_TTS.py`
8. Deactivate the virtual environment with `deactivate`