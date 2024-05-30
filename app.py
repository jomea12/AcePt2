import streamlit as st
import sounddevice as sd
import numpy as np
import webrtcvad
import collections
import scipy.io.wavfile as wav
import openai
import pyttsx3

# Set your OpenAI API key
openai.api_key = 'your-openai-api-key'

# Function to record audio with VAD
def record_audio_vad(duration=30, fs=16000, vad_mode=1):
    vad = webrtcvad.Vad(vad_mode)
    audio_buffer = collections.deque(maxlen=int(fs / 100 * 1.5))
    print("Listening...")

    def callback(indata, frames, time, status):
        frame_duration = 30  # 30 ms frames
        frame_size = int(fs * frame_duration / 1000)  # Calculate frame size in samples
        indata = indata[:, 0]  # Use the first channel only
        for i in range(0, len(indata), frame_size):
            frame = indata[i:i + frame_size]
            if len(frame) < frame_size:
                break
            is_speech = vad.is_speech(frame.tobytes(), fs)
            audio_buffer.extend(frame)
            if is_speech:
                record_audio_vad.speaking = True
            elif record_audio_vad.speaking:
                record_audio_vad.speaking = False
                raise sd.CallbackStop()

    record_audio_vad.speaking = False
    with sd.InputStream(callback=callback, channels=1, samplerate=fs, dtype='int16'):
        sd.sleep(int(duration * 1000))

    return np.concatenate(audio_buffer)

# Function to save recorded audio
def save_audio(audio, fs, file_path='output.wav'):
    wav.write(file_path, fs, audio)

# Function to transcribe audio using Whisper API
def transcribe_audio(file_path='output.wav'):
    audio_file = open(file_path, 'rb')
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']

# Function to perform text-to-speech
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
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
st.write("Click the button to start a conversation.")

if st.button("Start Recording"):
    try:
        # Record audio with VAD
        audio = record_audio_vad()
        save_audio(audio, 16000)
        
        # Transcribe audio using Whisper API
        user_input = transcribe_audio()
        st.write(f"You said: {user_input}")
        
        # Get GPT-4 response
        gpt_response = get_gpt4_response(user_input)
        st.write(f"GPT-4 says: {gpt_response}")
        
        # Speak the response
        st.audio("output.wav")
        speak_text(gpt_response)

    except Exception as e:
        st.write(f"An error occurred: {e}")
