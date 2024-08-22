from openai import OpenAI
from dotenv import load_dotenv
import os
import streamlit as st

if 'openai' not in st.session_state:
    st.session_state['openai'] = None
if 'chat' not in st.session_state:
    st.session_state['chat'] = [{"role": "user", "content": ""},{"role": "assistant", "content": ""},{"role": "user", "content": ""},{"role": "assistant", "content": ""},{"role": "user", "content": ""},{"role": "assistant", "content": ""}]

st.title("AI Assistant 🧠")

if st.session_state['openai'] == None:
    load_dotenv()
    openai = OpenAI(
        api_key= os.getenv('kurtim_api_key'), # Refer to Create a secret key section
        base_url="https://cloud.olakrutrim.com/v1",
    )
    st.session_state['openai'] = openai

def chat(question): 
        
    chat_completion = st.session_state['openai'].chat.completions.create(
    model="Meta-Llama-3-8B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. You are given conversation history and the latest question from the user. Answer the question based on your knowledge or based on the conversation history if needed"},
        {"role": "user", "content": st.session_state['chat'][-6]["content"]},
        {"role": "assistant", "content": st.session_state['chat'][-5]["content"]},
        {"role": "user", "content": st.session_state['chat'][-4]["content"]},
        {"role": "assistant", "content": st.session_state['chat'][-3]["content"]},
        {"role": "user", "content": st.session_state['chat'][-2]["content"]},
        {"role": "assistant", "content": st.session_state['chat'][-1]["content"]},
        {"role": "user", "content": question}
    ],
    logit_bias= {2435: -100, 640: -100},
    max_tokens= 5000,
    temperature= 0, # Optional, Defaults to 1. Range: 0 to 2
    top_p= 1 # Optional, Defaults to 1. It is generally recommended to alter this or temperature but not both.
    )

    response = chat_completion.choices[0].message.content

    st.session_state['chat'].append({"role": "user", "content": question})
    st.session_state['chat'].append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)

    return response

for message in st.session_state['chat'][6:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("What's up?")    

if prompt : 
    with st.chat_message("user"):
        st.markdown(prompt)
    chat(prompt)
    
st.sidebar.title("Chat History Controls")
    # Clear chat history button in sidebar
if st.sidebar.button("Clear Chat History"):
    st.session_state['chat'] = [{"role": "user", "content": ""},{"role": "assistant", "content": ""},{"role": "user", "content": ""},{"role": "assistant", "content": ""},{"role": "user", "content": ""},{"role": "assistant", "content": ""}]
    st.sidebar.success("Chat history cleared!")
    for message in st.session_state['chat'][6:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
