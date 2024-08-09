# Rag POC

This repository is a giant POC testing grounds for working on RAG using python. 

## Pre-requisites 

To run this repo using VS code you will need to first run a few commands. Here are the steps :

1. Once you've cloned the repository open up VSCode and open the project folder.
2. Start the terminal and run the following commands :
   #### 1. Creating a virtual environment
       python -m venv .venv
   #### 2. Running the virtual environment
       .venv\scripts\activate
   #### 3. Installing all the required libraries into the virtual environment (Make sure virtual environment is enabled and you are in the main parent folder of the project)
       pip install -r requirements.txt

You also need to have Ollama running on your local with "llama3" and "mxbai-embed-large". If you want to use other models you can change the code to reflect the same :) 

To run ollama follow these steps : 

1. Download the ollama installer for windows from the ollama website
2. Run the installer :D
3. Once installation is complete open cmdprmpt or powershell whichever you prefer and run the following commands : (Here you can download any model you want by replacing the names in the command)

   #### 1. To install llama3
         ollama pull llama3
   #### 2. To install mxbai-embed-large
         ollama pull mxbai-embed-large

## Running stuff 

After the pre-reqs are complete just open any of the ipynb files and run the cells (Shift + Enter)
## Apps

This folder contains any full-stack python apps I may create for RAG

#### wikiRAG
It is a fully functioning RAG application where a user can provide a wikipedia url, and then ask questions about that article
###### To run this app, navigate to the Apps folder in the terminal and then use the folloqing command
      streamlit run wikiRAG.py

## Notebooks Folder 

The Notebooks folder contains all the python notebooks, here's what each of them hold : 

#### creatingVectorStores
This notebook is to create vector stores using 2 different embedding models and store them into a local folder withing the project. These indexes are then used in the other notebooks to prevent re-embedding of the data again and again

#### initialNotebook 
This is the most basic first implementation. Has a lot of comments for a new user to understand what goes on in a RAG pipeline

#### testingAlternatives and testingAlternatives2
These two files mimic what was done in the initialNotebook but is experimenting with different text-splitters, models, file-types etc

#### onePrinterFile and multiplePrinterFiles
These are notebooks for a very specific usecase and a particular set of files that I wanted to test the model on. As the names suggest one uses only one pdf file while the latter uses 7-8 pdf files as a knowledge base for the RAG model

#### holdingConversation and holdingConversationSelf
These are notebooks where there's no RAG, we are just trying to keep the LLMs chat history with us intact so that it can answer questions based on the previous conversation as well. The first file utilises langchain libraries while the latter is a more straight forward approach of keeping the chat history maintained

#### ragWithConversation and ragWithConversation2
Trying to integrate the RAG POC and the POCs for holding conversations with an LLM and trying to combine both to give a RAG which is capable of remembering it's conversation with the user 

#### rudeChatbot
Talk to that guy at your own risk

#### webBasedRAG and webBasedRAG2
These are still in progress, basically you enter any url and it scrapes the webpage to enable asking questions about the contents of the webpage

#### wikiRAG
This is a notebook which can be used to ask questions about any wiki article 

## Data Folder 

The data folder just contains data on which the RAG models are trained

## VectorStores Folder

This folder contains all of the vector embeddings for the different data used in the RAG models. I've kept them stored in local so that we don't have to train the models again and again since it's time consuming. All the notebooks except for the initialNotebook use the presaved data stores

## Chats Folder

Contains text files which hold the chat history of a few successfull runs with the models that have convesational capabilities

## Azure

This folder contains the method to call an Azure OpenAI service hosted on... well, Azure. There's 2 subfolders one contains the code to talk to a gpt model, the other is to make calls to Dalle3. The third folder is for talking to a chat bot which uses data given by us as it's grounding truth. (It doesn't work since we don't have working endppoints and keys, but the syntax is available if you wanna learn)


# Hosting a locally running LLM 

#### Make sure ollama is running 
      http://localhost:11434/

#### Start docker open webui container 
      http://localhost:3000/

#### Using ngrock (Make sure .exe is in ...AppData\Local\Microsoft\WindowsApps)
      ngrok http 3000

#### Using zrok (Make sure .exe is in ...AppData\Local\Microsoft\WindowsApps)
      zrok share public http://localhost:3000/

Copy and share the url to access the ui :D
