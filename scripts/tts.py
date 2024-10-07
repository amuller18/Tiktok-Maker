from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import logger
import env
import sys
import time
    
logger = logger.log(0)
class tts:
    def __init__(self):
        pass
    
    def payloadSizeValid(self, payload):
        if sys.getsizeof(payload) < 5120:
            return True
        else:
            raise Exception('Your text is greater than 5120 bytes and cannot be passed to IBM Watson.')

    def make_tts(self, text):
        if(self.payloadSizeValid(text)):
            logger.log('Payload Size Valid...')
            logger.start('TTS')
            authenticator = IAMAuthenticator(env.tts_ibm)
            text_to_speech = TextToSpeechV1(
                authenticator=authenticator
            )
            text_to_speech.set_service_url('https://api.us-east.text-to-speech.watson.cloud.ibm.com/instances/0d81e097-9ac6-47a2-9068-36acdd03dd5d')
            with open('TTS.wav', 'wb') as audio_file:
                audio_file.write(
                    text_to_speech.synthesize(
                        text,
                        voice='en-US_MichaelV3Voice',
                        accept='audio/wav',
                        rate_percentage=-10        
                    ).get_result().content)
            logger.end('TTS')
        
    def numberOfParagraphs(self):
        pass