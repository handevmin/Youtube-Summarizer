from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pytube import YouTube
from moviepy.editor import *
from Clova import ClovaSpeechClient
import os

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UrlData(BaseModel):
    url: str

@app.post("/api/analyze")
async def analyze_audio(data: UrlData):
    video_url = data.url

    # pytube를 사용하여 유튜브 비디오 다운로드
    yt = YouTube(video_url)
    video = yt.streams.filter(file_extension='mp4').first()
    downloaded_file = video.download(filename='downloaded_video.mp4')

    # moviepy를 사용하여 다운로드한 비디오 파일에서 오디오 추출
    clip = VideoFileClip(downloaded_file)
    clip.audio.write_audiofile("audio.wav")
    clip.close()

    # Clova Speech API를 사용하여 STT 수행
    res = ClovaSpeechClient().req_upload(file='audio.wav', completion='sync')
    result = res.json()
    print(result)

    # Extract speaker-segmented results
    segments = result.get('segments', [])
    speaker_segments = []
    for segment in segments:
        speaker_label = segment['speaker']['label']
        text = segment['text']
        speaker_segments.append({'speaker': speaker_label, 'text': text})

    doc = ""
    # Print speaker-segmented results
    for speaker_segment in speaker_segments:
        speaker_label = speaker_segment['speaker']
        text = speaker_segment['text']
        print(f'Speaker {speaker_label}: {text}')
        doc+=text + " "

    # 임시 파일 삭제
    os.remove(downloaded_file)
    os.remove("audio.wav")

    return {"text": doc}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)