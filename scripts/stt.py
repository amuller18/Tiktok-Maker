from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import env
import threading
import logging

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

apikey = env.ibm_key
url = 'https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/81b73d9b-0b8e-440d-a010-80ff02a5fd96'

authenticator = IAMAuthenticator(env.stt_ibm)
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url(url)

def format_time(seconds):
    """Convert seconds to SRT timestamp format."""
    millis = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"

class MyRecognizeCallback(RecognizeCallback):
    def on_data(self, data):
        with open('subtitles.srt', 'w') as subtitles:
            for i, result in enumerate(data['results'][0]['alternatives'][0]['timestamps']):
                word = result[0]
                start_time = result[1]
                end_time = result[2]

                subtitles.write(f"{i}\n")
                subtitles.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
                subtitles.write(f"{word}\n\n")

    def on_error(self, error):  
        print(f'Error received: {error}')

def speech_to_text_func(audio_file):
    with open(audio_file, 'rb') as audio_file:
        audio_source = AudioSource(audio_file)
        callback = MyRecognizeCallback()
        
        def recognize():
            speech_to_text.recognize_using_websocket(
                audio=audio_source,
                content_type='audio/wav',
                recognize_callback=callback,
                model='en-US_BroadbandModel',
                timestamps=True,
                max_alternatives=1
            )
        
        recognize_thread = threading.Thread(target=recognize)
        recognize_thread.start()
        recognize_thread.join()
