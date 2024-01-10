from google.cloud import speech
import os

def transcribe_audio(localFile_path):
    """Transcribes local audio file using Speech-to-Text API."""
    client = speech.SpeechClient()
    with open(localFile_path, 'rb') as audio_file:
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


def get_transcript(gcs_response, bin_size=0.5):
    # gcs_response is the json response from the speech-to-text api call
    # bin_size is the interval in seconds in which we want to split the response into
    transcript = []
    current_sentence = []
    current_sentence_start = None
    current_sentence_end = None

    for result in gcs_response.results:
        # google responses have alternative transcriptions in which we selected the one the model is most confident in (alternatives[0])
        alternative = result.alternatives[0]
        for word_info in alternative.words:
            # info we have from the json response
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time

            # is this the first sentence? if so, need to instantiate the current_sentence start and end times.
            if current_sentence_start is None:
                current_sentence_start = start_time
                current_sentence_end = start_time

            # does current word belong in this bin or next one?
            if current_sentence_end.total_seconds() - current_sentence_start.total_seconds() > bin_size:
                transcript.append(((current_sentence_start.total_seconds(), current_sentence_end.total_seconds()),
                                   " ".join(current_sentence)))
                current_sentence = []
                current_sentence_start = start_time

            current_sentence.append(word)
            current_sentence_end = end_time

    # Add the last sentence
    if current_sentence:
        transcript.append(((current_sentence_start.total_seconds(), current_sentence_end.total_seconds()),
                           " ".join(current_sentence)))

    return transcript

base_dir = '..'
audio_dir = os.path.join(base_dir, 'data/scraped_audio')
transcripts_dir = os.path.join(base_dir, 'data/transcripts')
os.makedirs(transcripts_dir, exist_ok=True)

# Process each audio file
for audio_file in os.listdir(audio_dir):
    if audio_file.endswith('.mp3'):
        audio_path = os.path.join(audio_dir, audio_file)
        transcript_path = os.path.join(transcripts_dir, os.path.splitext(audio_file)[0] + '.txt')
        response = transcribe_audio(audio_path)
        transcript = get_transcript(response)

        with open(transcript_path, 'w') as file:
            for start_end, sentence in transcript:
                file.write(f"{start_end}: {sentence}\n")

        print(f"Transcript saved for {audio_file}")