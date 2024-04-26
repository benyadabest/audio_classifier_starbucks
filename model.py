import requests
import streamlit as st
import io
from st_audiorec import st_audiorec
import string


API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query_recor(audio_data):
    response = requests.post(API_URL, headers=headers, data=audio_data)
    return response.json()

def query_file(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

def normalize(text):
    return text.lower().translate(str.maketrans('', '', string.punctuation))

#testing
output = query_file("choc_cookie_order.flac")
print(output['text'])

st.title("Audio Classifcation: Starbucks Order Automation")
st.text("Speak your order, and we'll transcribe it for you!")

sample = st.button("Sample Order :musical_note::cookie:")

wav_audio_data = st_audiorec()


button = st.button("Order :coffee::croissant::white_check_mark::cool:")

if button:
    if wav_audio_data is not None:
        with st.spinner("Transcribing your order..."):
            output = query_recor(wav_audio_data)
            transcription = output['text'] if 'text' in output else "Error in transcription."
            st.text_area("Transcription Result:", transcription, height=150)
    else:
        st.error("Please record your order first!")

if sample:
    with st.spinner("Transcribing your order..."):
            st.audio("choc_cookie_order.flac")
            output = query_file("choc_cookie_order.flac")
            transcription = output['text'] if 'text' in output else "Error in transcription."
            st.text_area("Transcription Result:", transcription, height=150)

