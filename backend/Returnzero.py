import json
import requests
import time

# 인증 및 JWT 토큰 획득
resp = requests.post(
    'https://openapi.vito.ai/v1/authenticate',
    data={
        'client_id': 'sPHnfstUv1fcFn_5w8yb',
        'client_secret': 'C0hJH3bW7bUOnCd0g0GA7WaRhBCrdRxCYxvxKkZU'
    }
)
resp.raise_for_status()
YOUR_JWT_TOKEN = resp.json()['access_token']

# 오디오 파일 전송 및 전사 요청
config = {}
resp = requests.post(
    'https://openapi.vito.ai/v1/transcribe',
    headers={'Authorization': 'bearer '+YOUR_JWT_TOKEN},
    data={'config': json.dumps(config)},
    files={'file': open('audio.wav', 'rb')}
)
resp.raise_for_status()
TRANSCRIBE_ID = resp.json()['id']

# 폴링을 통해 전사 상태 확인
while True:
    resp = requests.get(
        f'https://openapi.vito.ai/v1/transcribe/{TRANSCRIBE_ID}',
        headers={'Authorization': 'bearer '+YOUR_JWT_TOKEN},
    )
    resp.raise_for_status()
    response_json = resp.json()

    # 전사 상태 확인
    if response_json['status'] == 'completed':
        # 전사 완료
        print("Transcription completed:", response_json)
        break
    elif response_json['status'] == 'failed':
        # 전사 실패
        print("Transcription failed:", response_json)
        break
    else:
        # 아직 진행 중
        print("Transcription in progress...")

    time.sleep(5)  # 5초 대기 후 다시 확인
