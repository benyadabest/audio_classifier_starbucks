import requests
import streamlit as st
from st_audiorec import st_audiorec


API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

#testing
output = query("choc_cookie_order.flac")
print(output['text'])

st.title("Audio Classifcation: Starbucks Order Automation")
st.text("Speech -> Text -> Link to Item")

uploaded_file = st.file_uploader("Upload Audio File!")
wav_audio_data = st_audiorec()


button = st.button("Order :coffee::croissant::white_check_mark::cool:")

if button:
    if uploaded_file is not None:
        if wav_audio_data is not None:
            st.audio(wav_audio_data, format='audio/wav')
        with st.spinner("Loading..."):
            with open("temp_audio.flac", "wb") as f:
                f.write(uploaded_file.getvalue())

                output = query("temp_audio.flac")
                transcription = output['text'] if 'text' in output else "Error in transcription."

                st.text_area("Transcription Result:", transcription, height=150)
    else:
        st.error("Upload audio file first!!")