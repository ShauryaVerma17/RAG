import streamlit as st
from audio_recorder_streamlit import audio_recorder
from openai import OpenAI
import base64
from dotenv import load_dotenv
import os
import streamlit_analytics2 as streamlit_analytics
import requests
import json

load_dotenv()

openai = OpenAI(
    api_key= os.getenv('kurtim_api_key'), # Refer to Create a secret key section
    base_url="https://cloud.olakrutrim.com/v1",
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [('',''),('',''),('',''),('',''),('',''),('','')]
if 'query' not in st.session_state:
    st.session_state['query'] = ""

def transcribeAudio(audio_file):

    encoded_audio = base64.b64encode(audio_file).decode("utf-8")

    payload = {
    "modelName": "openai/whisper-large-v3", # DO NOT CHANGE this
    "file": encoded_audio, 
    "task": "transcribe", 
    "language": "english", # Source language of the audio
    "temperature": 0.0, # Optional, defaults to 0.0. Range - 0.0 to 2.0
    "responseFormat": "json", # Optional, defaults to json. Values - verbose_json (or) json
    "chunkType": "word" # Optional, defaults to sentence. Values - sentence (or) word
    }

    # Define the URL to the model server
    url = "https://cloud.olakrutrim.com/v1/audio/transcriptions"

    # Send the POST request
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    transcription = response.text

    return transcription

def chat(question): 
    
    global openai

    chat_completion = openai.chat.completions.create(
    model="Meta-Llama-3-8B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. You are given conversation history and the latest question from the user. Answer the question based on your knowledge or based on the conversation history if needed"},
        {"role": "user", "content": st.session_state['chat_history'][-6][-1]},
        {"role": "assistant", "content": st.session_state['chat_history'][-5][-1]},
        {"role": "user", "content": st.session_state['chat_history'][-4][-1]},
        {"role": "assistant", "content": st.session_state['chat_history'][-3][-1]},
        {"role": "user", "content": st.session_state['chat_history'][-2][-1]},
        {"role": "assistant", "content": st.session_state['chat_history'][-1][-1]},
        {"role": "user", "content": question}
    ],
    logit_bias= {2435: -100, 640: -100},
    max_tokens= 5000,
    temperature= 0, # Optional, Defaults to 1. Range: 0 to 2
    top_p= 1 # Optional, Defaults to 1. It is generally recommended to alter this or temperature but not both.
    )

    response = chat_completion.choices[0].message.content

    st.session_state['chat_history'].append(("User",question))
    st.session_state['chat_history'].append(("Assistant",response))


st.title("Talk to AI 🎙️")

recorded_audio = audio_recorder(text= "Click on the mic to talk to the AI Assistant (Click again to start processing your question)")

if recorded_audio : 
    question = transcribeAudio(recorded_audio)
    st.write(question)
    recorded_audio = None

# Sidebar for chat history
st.sidebar.title("Chat History")
for (user,message) in st.session_state['chat_history'][6:]:
    st.sidebar.text(f"{user}:{message}")

# Clear chat history button in sidebar
if st.sidebar.button("Clear Chat History"):
    st.session_state['chat_history'] = [('',''),('',''),('',''),('',''),('',''),('','')]
    st.sidebar.success("Chat history cleared!")