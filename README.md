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
   #### 3. Installing all the required libraries into the virtual environment
       pip install langchain langchain_community faiss-cpu pymupdf docarray unstructured tiktoken

You also need to have Ollama running on your local with "llama3" and "mxbai-embed-large". If you want to use other models you can change the code to reflect the same :) 
To run ollama follow these steps : 

1. Download the ollama installer for windows from the ollama website
2. Run the installer :D
3. Once installation is complete open cmdprmpt or powershell whichever you prefer and run the following commands : (Here you can download any model you want by replacing the names in the command)

   #### 1. To install llama3
         ollama pull llama3
   #### 2. To install mxbai-embed-large
         ollama pull mxbai-embed-large

## Runnning stuff 

After the pre-reqs are complete just open any of the ipynb files and run the cells (Shift + Enter)

## Notebooks Folder 

The Notebooks folder contains all the python notebooks, here's what each of them hold : 

#### initialNotebook 
This is the most basic first implementation. Has a lot of comments for a new user to understand what goes on in a RAG pipeline

#### testingAlternatives and testingAlternatives2
These two files mimic what was done in the initialNotebook but is experimenting with different text-splitters, models, file-types etc

#### onePrinterFile and multiplePrinterFiles
These are notebooks for a very specific usecase and a particular set of files that I wanted to test the model on. As the names suggest one uses only one pdf file while the latter uses 7-8 pdf files as a knowledge base for the RAG model

#### holdingConversation and holdingConversationSelf
These are notebooks where there's no RAG, we are just trying to keep the LLMs chat history with us intact so that it can answer questions based on the previous conversation as well. The first file utilises langchain libraries while the latter is a more straight forward approach of keeping the chat history maintained

#### ragWithConversation
Trying to integrate the RAG POC and the POCs for holding conversations with an LLM and trying to combine both to give a RAG which is capable of remembering it's conversation with the user 

#### rudeChatbot
Talk to that guy at your own risk

## Data Folder 

The data folder just contains data on which the RAG models are trained

## VectorStores Folder

This folder contains all of the vector embeddings for the different data used in the RAG models. I've kept them stored in local so that we don't have to train the models again and again since it's time consuming

## RAGChats Folder

Contains text files which hold the chat history of a few successfull runs with the RAG model that has convesational capabilities
