from google.cloud import speech
import os

def transcribe_audio(file_path):
    """
    Transcribes local audio file using Google Cloud Speech-to-Text API.
    
    Parameter:
    file_path - the path to the audio file (string)
    """
    client = speech.SpeechClient()
    with open(file_path, 'rb') as audio_file:
        content = audio_file.read()
    
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code="en-US",
        model="latest_long",
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=90)

    return response

def get_transcript(gcs_response, bin_size=0.3):
    """
    Returns the transcript of an audio file given the json response from the
    speech-to-text API call.

    Parameters:
    gcs_response - the json response from the speech-to-text API call
    bin_size - the interval in seconds in which we want to split the response into (float)
    """
    transcript = []
    current_sentence = []
    current_sentence_start = None
    current_sentence_end = None
    defer_split = False  # Flag to defer splitting after "part"

    for result in gcs_response.results:
        alternative = result.alternatives[0]

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time

            if current_sentence_start is None:
                current_sentence_start = start_time
                current_sentence_end = start_time

            if word.lower() == "part":
                defer_split = True  # Defer the next split

            if defer_split and len(current_sentence) > 1:
                if current_sentence[-1].lower() == "part":
                    current_sentence.append(word)
                    current_sentence_end = end_time
                    continue
                else:
                    defer_split = False  # Reset flag after adding the word following "part"

            if current_sentence_end.total_seconds() - current_sentence_start.total_seconds() > bin_size and not defer_split:
                transcript.append(((current_sentence_start.total_seconds(), current_sentence_end.total_seconds()),
                                   " ".join(current_sentence)))
                current_sentence = [word]  # Start new sentence with current word
                current_sentence_start = start_time
            else:
                current_sentence.append(word)

            current_sentence_end = end_time

    # Add the last sentence
    if current_sentence:
        transcript.append(((current_sentence_start.total_seconds(), current_sentence_end.total_seconds()),
                           " ".join(current_sentence)))

    return transcript


# Create directory paths
base_dir = '..'
audio_dir = os.path.join(base_dir, 'data/scraped_audio')
transcripts_dir = os.path.join(base_dir, 'data/transcripts')

# Ensure transcript directory exists
os.makedirs(transcripts_dir, exist_ok=True)

# Process each audio file
for audio_file in os.listdir(audio_dir):
    # Check if the audio file is mp3
    if audio_file.endswith('.mp3'):
        audio_path = os.path.join(audio_dir, audio_file)
        transcript_path = os.path.join(transcripts_dir, os.path.splitext(audio_file)[0] + '.txt')

        # Create transcript
        response = transcribe_audio(audio_path)
        transcript = get_transcript(response)

        # Save transcript
        with open(transcript_path, 'w') as file:
            for start_end, sentence in transcript:
                file.write(f"{start_end}: {sentence}\n")

        print(f"Transcript saved for {audio_file}")