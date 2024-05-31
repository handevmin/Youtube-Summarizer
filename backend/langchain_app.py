import os
from openai import OpenAI

# Web UI
import streamlit as st

# To handle multimedia
import ffmpeg
from pytube import YouTube
import yt_dlp
import subprocess
from moviepy.editor import *

# Text analysis
from langchain import LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document

from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

from Clova import ClovaSpeechClient

from datetime import timedelta


load_dotenv()  # .env 파일에서 환경 변수 로드

# New function to convert seconds to (hours, minutes, seconds)
def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{int(hours)}:{int(minutes)}:{int(seconds)}"

# Function to create a trimmed video clip

def make_clip_video(url, start_t, end_t):
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc().first()
    download_path = stream.download()  # Downloads the video to the current working directory

    # Load the downloaded video file
    original_clip = VideoFileClip(download_path)
    # Trim the video
    trimmed_clip = original_clip.subclip(start_t, end_t)
    trimmed_clip_path = "trimmed_audio.mp4"
    trimmed_clip.write_videofile(trimmed_clip_path, codec='libx264', audio_codec='aac')
    original_clip.close()
    trimmed_clip.close()

    # Optionally delete the original downloaded video file to save space
    os.remove(download_path)

    return trimmed_clip_path


def extract_audio_segment(input_audio_path, start_time, end_time, output_audio_path):
    """
    Extracts a segment from an audio file.

    Parameters:
    - input_audio_path: Path to the input audio file.
    - start_time: Start time of the segment in seconds.
    - end_time: End time of the segment in seconds.
    - output_audio_path: Path to save the extracted audio segment.
    """
    audio_clip = AudioFileClip(input_audio_path).subclip(start_time, end_time)
    audio_clip.write_audiofile(output_audio_path, codec='pcm_s16le')
    audio_clip.close()
def text_custom(font_size, text):
    """
    font_size := ['b', 'm', 's']
    """
    result = f'<p class="{font_size}-font">{text}</p>'
    return result


def main():
    st.set_page_config(
        layout="wide", page_title=f"STT & AI Analysis Demo by AIC :sunglass:"
    )

    # reference
    ## https://discuss.streamlit.io/t/change-input-text-font-size/29959/4
    ## https://discuss.streamlit.io/t/change-font-size-in-st-write/7606/2
    st.markdown(
        """<style>.b-font {font-size:25px !important;}</style>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<style>.m-font {font-size:20px !important;}</style>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<style>.s-font {font-size:15px !important;}</style>""",
        unsafe_allow_html=True,
    )
    tabs_font_css = """<style>div[class*="stTextInput"] label {font-size: 15px;color: black;}</style>"""
    st.write(tabs_font_css, unsafe_allow_html=True)

    st.title("STT & Text Analysis")
    t = "사용을 위해 OpenAI API key를 입력해주세요."
    st.markdown(text_custom("m", t), unsafe_allow_html=True)

    api_key = st.text_input(
        "Enter Open AI Key.",
        placeholder="sk-...",
        type="password",
    )

    with st.sidebar:
        chunk_size = st.slider(
            "Chunk size",
            0,
            1500,
            500,
        )

        overlap_size = st.slider(
            "Overlap size",
            0,
            500,
            150,
        )

        stt_model = st.selectbox(label="STT Model", options=["whisper-1"])

        embeddeing_model = st.selectbox(
            label="Embedding Model", options=["text-embedding-ada-002"]
        )

        summarization_model = st.selectbox(
            label="Summarization LLM Model",
            options=["gpt-4-0125-preview", "gpt-3.5-turbo-0125"],
        )

        qa_model = st.selectbox(
            label="QA LLM Model", options=["gpt-4-0125-preview", "gpt-3.5-turbo-0125"]
        )

        temperature = st.slider(
            "Temperature",
            0.0,
            1.0,
            0.01,
        )

        chain = st.radio(label="Chain type", options=["stuff", "map_reduce"])

        st.markdown(
            """
            **Code:** 
            [*Github Repo*](https://github.com/jskim0406/STT_ChatGPT_w_langchain)
            """
        )

    t = "Audio를 추출하고, 분석하고자 하는 Youtube 영상의 URL을 아래에 입력해주세요."
    st.markdown(text_custom("m", t), unsafe_allow_html=True)

    t = '해당 영상의 오디오(speech)에서 Text를 추출할 것입니다.'
    st.markdown(text_custom("m", t), unsafe_allow_html=True)

    # 영상 URL 입력
    youtube_url = st.text_input(
        label="Youtube URL을 입력해주세요.",
        value="https://www.youtube.com/watch?v=s8EKVNcD1ko",
    )

    if youtube_url:
        width = 40
        side = max((100 - width) / 2, 0.01)
        _, container, _ = st.columns([side, width, side])
        container.video(data=youtube_url)
    else:
        t = "Youtube URL을 입력하면 영상이 Embedding됩니다. :)"
        st.markdown(text_custom("s", t), unsafe_allow_html=True)

    st.header("Phase 1: Audio Extraction")
    t = "Youtube Video에서 Audio를 추출합니다."
    st.markdown(text_custom("m", t), unsafe_allow_html=True)
    t = "Youtube에서 Audio를 추출하기 위해 'Pytube'라는 python 패키지를 활용합니다."
    st.markdown(text_custom("s", t), unsafe_allow_html=True)


    if os.path.exists("segment_audio.wav"):
        # 파일 삭제
        os.remove("segment_audio.wav")

    if st.button("Get Audio. START !"):
        with st.spinner("Audio Extraction in progress.."):
            selected_video = YouTube(youtube_url)

            stream_url = selected_video.streams.all()[
                0
            ].url  # Get the URL of the video stream

            # AudioFileClip 객체를 생성합니다.
            audio_clip = VideoFileClip(stream_url)

            # 오디오를 WAV 형식으로 저장합니다.
            audio_clip.audio.write_audiofile("audio.wav", codec='pcm_s16le')

            # audio, err = (
            #     ffmpeg.input(stream_url)
            #     .output(
            #         "pipe:", format="wav", acodec="pcm_s16le"
            #     )  # Select WAV output format, and pcm_s16le auidio codec. My add ar=sample_rate
            #     .run(capture_stdout=True)
            # )

            audio_f_name = "audio"

        st.success(f'Audio extraction & and Saved in "{audio_f_name}" is Done!')

        st.audio(audio_f_name + ".wav")
    print("File Size(audio.wav): ", os.path.getsize("audio.wav"), 'bytes')

    st.header("(Optional) Select Audio Segment")
    start_time = st.number_input("Start Time (in seconds):", min_value=0.0, value=0.0, step=0.1)
    end_time = st.number_input("End Time (in seconds):", min_value=0.0, value=0.0, step=0.1)
    if st.button("Extract Audio Segment"):
        extract_audio_segment("audio.wav", start_time, end_time, "segment_audio.wav")
        st.success("Audio segment extracted successfully.")
        st.audio("segment_audio.wav")


    # Phase 2: Text Extraction(STT) : CLOVA 활용
    st.header("Phase 2: Text Extraction(STT)")
    if st.button("STT. START !"):
        if os.path.exists("segment_audio.wav"):
            audio_f_name = "segment_audio"
            print("File Size(segment_audio.wav): ",os.path.getsize("segment_audio.wav"), 'bytes')
        else:
            audio_f_name = "audio"
        audio_file_path = f"{audio_f_name}.wav"  # 'audio.wav' 파일 사용
        res = ClovaSpeechClient().req_upload(file=audio_file_path, completion='sync')
        result = res.json()

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

        print(doc)
        text_f_name = "extracted.txt"
        with open("extracted.txt", "w") as f:
            f.write(doc)
        st.success(f'STT is Done & Saved in "{text_f_name}"!')

        with st.expander("Extracted texts..", expanded=True):
            doc

        # Add download button for the extracted text file
        with open(text_f_name, "rb") as file:
            btn = st.download_button(
                label="Download Extracted Text",
                data=file,
                file_name=text_f_name,
                mime="text/plain"
            )

    # Whisper 활용
    # global txt
    # txt = None

    # st.header("Phase 2: Text Extraction(STT)")
    # t = "STT는 OpenAI의 Whisper-1 모델을 사용합니다."
    # st.markdown(text_custom("m", t), unsafe_allow_html=True)
    # t = "구현의 간편성을 위해 API로 호출해 제작합니다."
    # st.markdown(text_custom("s", t), unsafe_allow_html=True)
    #
    # if st.button("STT. START !"):
    #     # STT with OpenAI API
    #     if os.path.exists("segment_audio.wav"):
    #         audio_f_name = "segment_audio"
    #         print("File Size(segment_audio.wav): ",os.path.getsize("segment_audio.wav"))
    #     else:
    #         audio_f_name = "audio"
    #     audio_file_path = f"{audio_f_name}.wav"  # 'audio.wav' 파일 사용
    #
    #     os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
    #
    #     client = OpenAI()
    #
    #     # 오디오 파일을 바이너리 모드로 열기
    #     with open(audio_file_path, "rb") as audio_file:
    #         with st.spinner("STT in progress.."):
    #             transcript = client.audio.transcriptions.create(
    #                 model="whisper-1",
    #                 file=audio_file
    #             )
    #     print(transcript)
    #     txt = transcript.text
    #
    #     text_f_name = "extracted.txt"
    #     with open("extracted.txt", "w") as f:
    #         f.write(txt)
    #     st.success(f'STT is Done & Saved in "{text_f_name}"!')
    #
    #     with st.expander("Extracted texts..", expanded=True):
    #         txt

    # Phase 3: Text Analysis process(w/ LangChain)
    st.header("Phase 3: Text Analysis process(w/ LangChain)")
    st.markdown(
        "사용할 모델은 OpenAI의 ChatGPT입니다."
    )

    st.subheader("Phase 3-1: Text summarization")
    t = "Text Summarization에 사용할 모델은 왼쪽 Sidebar에서 선택할 수 있습니다."
    st.markdown(text_custom("m", t), unsafe_allow_html=True)
    text_f_name = "extracted"
    if os.path.isfile(f"{text_f_name}.txt"):
        with st.expander("Extracted texts..", expanded=False):
            f = open(f"{text_f_name}.txt", "r")
            txt_ext = f.read()
            txt_ext
            f.close()

    if st.button("Summarization. START !"):
        with st.spinner("OpenAI model loading.."):
            llm = ChatOpenAI(
                temperature=temperature,
                model_name=summarization_model,
                openai_api_key=api_key
            )
            st.success(f'OpenAI model("{summarization_model}") is loaded.')


        with st.spinner("Chunking is in progress.."):
            text_splitter = CharacterTextSplitter(
                chunk_size=chunk_size, separator=".", chunk_overlap=overlap_size
            )
            texts = text_splitter.split_text(txt_ext)
            docs = [Document(page_content=t) for t in texts]
        st.success(f"Chunking is Done.")

        with st.spinner("Summarization is in progress.."):
            prompt_template = """Write a comprehensive summary about the given texts in KOREAN:\n\n{text}."""
            PROMPT = PromptTemplate(
                template=prompt_template, input_variables=["text"]
            )
            if chain == "stuff":
                chain = load_summarize_chain(
                    llm, chain_type=chain, prompt=PROMPT, verbose=True
                )
            elif chain == "map_reduce":
                chain = load_summarize_chain(
                    llm,
                    chain_type=chain,
                    map_prompt=PROMPT,
                    combine_prompt=PROMPT,
                    verbose=True,
                )
            sum_txt = chain.run(docs)
        st.success(f"Summarization is Done.")

        with st.expander("Show me summarized text..", expanded=True):
            sum_txt

        with open("summarized_extracted.txt", "w") as f:
            f.write(sum_txt)

    st.subheader("Phase 3-2: QA based on extracted text")
    t = "Question Answering on TEXT에 사용할 모델은 왼쪽 Sidebar에서 선택할 수 있습니다."
    st.markdown(text_custom("m", t), unsafe_allow_html=True)
    if os.path.isfile("extracted.txt"):
        with st.expander("Extracted texts..", expanded=False):
            f = open("extracted.txt", "r")
            txt_ext = f.read()
            txt_ext
            f.close()

    # if os.path.isfile("summarized_extracted.txt"):
    #     with st.expander("Summarized texts..", expanded=False):
    #         f = open("summarized_extracted.txt", "r")
    #         txt_ext = f.read()
    #         txt_ext
    #         f.close()

    global query
    query = st.text_input("질문을 입력해주세요.", placeholder=f"Ask me anything from your text.")

    if query:
        if st.button("Question Answering. START !"):
            with st.spinner("Chunking is in progress.."):
                text_splitter = CharacterTextSplitter(
                    chunk_size=chunk_size, separator=".", chunk_overlap=overlap_size
                )
                texts = text_splitter.split_text(txt_ext)
                docs = [Document(page_content=t) for t in texts]
            st.success(f"Chunking is Done.")

            with st.spinner("OpenAI Embedding is loading & Embedding in progress.."):
                embeddings = OpenAIEmbeddings(
                    openai_api_key=api_key, model=embeddeing_model
                )
                docsearch = Chroma.from_documents(docs, embeddings)
            st.success(f"Embedding is Done. VectorDB is created.")

            with st.spinner("Question Answering functionality is in progress.."):
                model_name = qa_model
                llm = ChatOpenAI(
                    temperature=temperature,
                    model_name=model_name,
                    openai_api_key=api_key
                )
                qa = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type=chain,
                    retriever=docsearch.as_retriever(),
                    verbose=True
                )
                st.success(f"Question Answering is ready.")

                with st.spinner("Please wait for the answer :) "):
                    query += " 한국어로 답변해주세요. Answer in KOREAN."
                    ansewr = qa.run(query)
                st.success(f"Done.")

                with st.expander("Answer is ..", expanded=False):
                    ansewr


if __name__ == "__main__":
    main()