import requests
from dotenv import load_dotenv
import json


class ClovaSpeechClient:
    # # Clova Speech invoke URL
    invoke_url = 'https://clovaspeech-gw.ncloud.com/external/v1/7135/e5df128a9eaa8264b5bacef4c7991abdf8e8bbeb03a13e91460ed3cae346810e'
    # Clova Speech secret key
    secret = os.getenv('CLOVA_SPEECH_SECRET_KEY')

    # free version
    # Clova Speech invoke URL
    # invoke_url = 'https://clovaspeech-gw.ncloud.com/external/v1/7042/f44e85c4b8ea2addc796f8beab6600e801d767ccd26c800dce6d88fdaa5eb4e6'
    # # Clova Speech secret key
    # secret = '8c99929f63ea4b9c9a265b27d8c7f1f0'

    def req_url(self, url, completion, callback=None, userdata=None, forbiddens=None, boostings=None, wordAlignment=True, fullText=True, diarization=None, sed=None):
        request_body = {
            'url': url,
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
            'sed': sed,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'Content-Type': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        return requests.post(headers=headers,
                             url=self.invoke_url + '/recognizer/url',
                             data=json.dumps(request_body).encode('UTF-8'))

    def req_object_storage(self, data_key, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                           wordAlignment=True, fullText=True, diarization=None, sed=None):
        request_body = {
            'dataKey': data_key,
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
            'sed': sed,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'Content-Type': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        return requests.post(headers=headers,
                             url=self.invoke_url + '/recognizer/object-storage',
                             data=json.dumps(request_body).encode('UTF-8'))

    def req_upload(self, file, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                   wordAlignment=True, fullText=True, diarization=None, sed=None):
        request_body = {
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
            'sed': sed,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        print(json.dumps(request_body, ensure_ascii=False).encode('UTF-8'))
        files = {
            'media': open(file, 'rb'),
            'params': (None, json.dumps(request_body, ensure_ascii=False).encode('UTF-8'), 'application/json')
        }
        response = requests.post(headers=headers, url=self.invoke_url + '/recognizer/upload', files=files)
        return response

if __name__ == '__main__':
    res = ClovaSpeechClient().req_upload(file='audio.wav', completion='sync')
    result = res.json()

    # Extract speaker-segmented results
    segments = result.get('segments', [])
    speaker_segments = []
    for segment in segments:
        speaker_label = segment['speaker']['label']
        text = segment['text']
        speaker_segments.append({'speaker': speaker_label, 'text': text})

    # Print speaker-segmented results
    for speaker_segment in speaker_segments:
        speaker_label = speaker_segment['speaker']
        text = speaker_segment['text']
        print(f'Speaker {speaker_label}: {text}')