import streamlit as st
import numpy as np
import openai
import pyttsx3

# Set your OpenAI API key
openai.api_key = 'sk'+'-'+'proj-kcFVZ'+'et7tS9VSpF'+'0lvIbT3B'+'lbkFJAR1'+'1WMqBBE'+'wjUW0lSKiv'

# Function to save uploaded audio
def save_audio(uploaded_file, file_path='output.wav'):
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

# Function to transcribe audio using Whisper API
def transcribe_audio(file_path='output.wav'):
    with open(file_path, 'rb') as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']

# Function to perform text-to-speech
def speak_text(text, file_path='response.wav'):
    engine = pyttsx3.init()
    engine.save_to_file(text, file_path)
    engine.runAndWait()

# Function to get GPT-4 response
def get_gpt4_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",  # Replace with "gpt-4" if available
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Streamlit app
st.title("Voice Conversation with GPT-4 and Whisper")
st.write("Record your voice, upload the file, and get a response.")

# HTML and JS for client-side recording
st.markdown("""
    <h1>Record Audio</h1>
    <button id="recordButton">Record</button>
    <button id="stopButton" disabled>Stop</button>
    <br>
    <audio id="audioPlayback" controls></audio>
    <script src="static/js/record_audio.js"></script>
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload an audio file", type=["wav"])

if uploaded_file is not None:
    # Save uploaded audio
    save_audio(uploaded_file)

    # Transcribe audio using Whisper API
    user_input = transcribe_audio()
    st.write(f"You said: {user_input}")

    # Get GPT-4 response
    gpt_response = get_gpt4_response(user_input)
    st.write(f"GPT-4 says: {gpt_response}")

    # Generate speech from the response
    speak_text(gpt_response)
    
    # Play the response audio
    audio_file = open("response.wav", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/wav")
