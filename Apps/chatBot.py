from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai = OpenAI(
    api_key= os.getenv('kurtim_api_key'), # Refer to Create a secret key section
    base_url="https://cloud.olakrutrim.com/v1",
)

chatHistory = ["","","","","",""]

def chat(question): 
    
    global chatHistory
    
    chat_completion = openai.chat.completions.create(
    model="Meta-Llama-3-8B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. You are given conversation history and the latest question from the user. Answer the question based on your knowledge or based on the conversation history if needed"},
        {"role": "user", "content": chatHistory[-6]},
        {"role": "assistant", "content": chatHistory[-5]},
        {"role": "user", "content": chatHistory[-4]},
        {"role": "assistant", "content": chatHistory[-3]},
        {"role": "user", "content": chatHistory[-2]},
        {"role": "assistant", "content": chatHistory[-1]},
        {"role": "user", "content": question}
    ],
    logit_bias= {2435: -100, 640: -100},
    max_tokens= 5000,
    temperature= 0, # Optional, Defaults to 1. Range: 0 to 2
    top_p= 1 # Optional, Defaults to 1. It is generally recommended to alter this or temperature but not both.
    )

    response = chat_completion.choices[0].message.content

    chatHistory.append(question)
    chatHistory.append(response)

    return response

while True:
    query = input("Enter you query : ")
    if query == "quit":
        break
    else : 
        print("Assistant : \n" + chat(query) + "\n")