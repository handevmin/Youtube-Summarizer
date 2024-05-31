from googleapiclient.discovery import build
from pytube import YouTube
from moviepy.editor import *
from Clova import ClovaSpeechClient
from prompts import youtube_map, youtube_combine
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
import tiktoken
from langchain.text_splitter import TokenTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from elbow import *
from sklearn.cluster import KMeans
from langchain.schema import Document
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()  # .env 파일 로드

api_key = os.getenv('OPENAI_API_KEY')
youtube_api_key = os.getenv('YOUTUBE_API_KEY')

# 유튜브 API 설정
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

def main():
    # # 검색할 키워드 설정
    # keyword = '인공지능'  # 여기에 검색할 키워드를 입력하세요
    #
    # # 키워드에 따른 유튜브 검색 수행
    # search_request = youtube.search().list(q=keyword, part='snippet', maxResults=1, type='video')
    # search_response = search_request.execute()
    #
    # # 검색 결과에서 첫 번째 동영상 URL 가져오기
    # video_id = search_response['items'][0]['id']['videoId']
    # video_url = 'https://www.youtube.com/watch?v=' + video_id
    # print(video_url)
    #
    # # pytube를 사용하여 유튜브 비디오 다운로드
    # yt = YouTube(video_url)
    # video = yt.streams.filter(file_extension='mp4').first()
    # downloaded_file = video.download(filename='downloaded_video.mp4')
    #
    # # moviepy를 사용하여 다운로드한 비디오 파일에서 오디오 추출
    # clip = VideoFileClip(downloaded_file)
    # clip.audio.write_audiofile("audio.wav")
    #
    #
    # res = ClovaSpeechClient().req_upload(file='audio.wav', completion='sync')
    # result = res.json()
    #
    # # Extract speaker-segmented results
    # segments = result.get('segments', [])
    # speaker_segments = []
    # for segment in segments:
    #     speaker_label = segment['speaker']['label']
    #     text = segment['text']
    #     speaker_segments.append({'speaker': speaker_label, 'text': text})
    #
    # doc = ""
    # # Print speaker-segmented results
    # for speaker_segment in speaker_segments:
    #     speaker_label = speaker_segment['speaker']
    #     text = speaker_segment['text']
    #     print(f'Speaker {speaker_label}: {text}')
    #     doc+=text + " "

    doc = """
    Speaker 1: GPT를 만든 오픈ai사가 글을 입력하면 내용에 맞는 동영상을 만들어주는 인공지능 모델을 공개했습니다.
    Speaker 1: 현실 세계를 직접 촬영한 영상이나 그래픽 작업으로 만든 애니메이션과 구분이 어려울 정도로 정교하고 생생한데요. 기술의 발달과 함께 풀어야 할 과제도 대두되고 있
    습니다. 최소라 기자입니다.
    Speaker 2: 멋지게 차려 입은 여성이 거리를 걷고 있습니다.
    Speaker 2: 피부결과 주름, 머리카락까지 마치 실제 사람을 촬영한 것 같지만 인공지능이 순수 창조한 동영상입니다.
    Speaker 2: 멋진 여성이 네온사인과 간판으로 가득한 도쿄 거리를 걷고 있다와 같은 간단한 문장 6개만으로 생성해낸 겁니다.
    Speaker 2: 이미 멸종한 동물인 매머드가 눈보라를 일으키며 설원을 달리는 영상부터
    Speaker 2: 절벽으로 하얗게 부서지는 파도의 모습을 드론으로 촬영한 듯한 영상까지 모두 오픈ai의 새로운 모델 소라가 만들어낸 겁니다.
    Speaker 2: 소라는 글을 동영상으로 만들어주는 이른바 텍스트 투 비디오 모델인데 글로 된 요청을 이해할 뿐 아니라
    Speaker 2: 글에 묘사된 것들이 실제 세계에서 어떻게 존재하는지까지 이해한다고 오픈ai는 설명했습니다.
    Speaker 2: 앞서 2022년 구글 딥마인드도 유사한 모델 페나키를 공개했고, 런웨이도 젠투를 서비스하고 있지만
    Speaker 2: 화질과 품질이 모두 조악한 수준입니다. 소라가 생성한 영상에도 아직 오게티가 있기는 하지만 쉽게 알아차리지 못할 수준인 데다
    Speaker 2: 동영상 화질도 HD급 이상의 고해상도입니다.
    Speaker 2: 문제는 이 같은 고성능 인공지능이 부적절한 용도나 사회 혼란을 초래하는 쪽으로 악용될 수 있다는 겁니다.
    Speaker 3: 그래서 이 기술로 생성한 음란 영상, 가짜 뉴스가 사회적으로 여러 문제를 일으키고 있죠.
    Speaker 3: df 기술은 빠르게 발전하고 있으며 사람들이 감지하기 어려운 수준까지 왔지만은 감지하는 기술도 이 못지않게 빠르게 발전하고 있어
    Speaker 3: 디페이크 알고리즘과 감지 알고리즘 간의 경쟁은 끝이 없을 것으로 예상이 됩니다.
    Speaker 2: 오픈ai는 소라의 안전성 확보를 위해 전문가 검증을 거치고 있다며 소라는 폭력, 혐오, 저작권 침해,
    Speaker 2: 성적 콘텐츠 요청은 물론 유명인과 유사한 이미지 생성 요청을 거절할 것이라며 딥페이크 문제 해소 의지를 보였습니다.
    Speaker 2: 또 이번 기술 공개는 대중이 인공지능의 능력을 알 수 있도록 조기에 공개한 것이라며 소라의 정식 출시 시기는 밝히지 않았습니다.
    Speaker 2: YTN 사이언스 최소라입니다.
    """

    # GPT 모델 초기화
    llm = ChatOpenAI(openai_api_key=api_key, temperature=0, max_tokens=1000, model_name='gpt-4-0125-preview')

    # 요약을 위한 프롬프트 템플릿 생성
    prompt_template = PromptTemplate(template="요약: {{text}}", input_variables=['text'])

    # 요약 체인 로드
    summarize_chain = load_summarize_chain(llm=llm, chain_type='stuff', prompt=prompt_template)

    # 문서 생성 및 요약
    document = Document(page_content=doc)
    summary = summarize_chain.run([document])

    print(summary)


main()