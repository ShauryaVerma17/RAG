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
       pip install langchain langchain_community faiss-cpu pymupdf docarray unstructured

You also need to have Ollama running on your local with "llama3" and "mxbai-embed-large". If you want to use other models you can change the code to reflect the same :) 

## Runnning stuff 

After the pre-reqs are complete just open any of the ipynb files and run the cells (Shift + Enter)

## Different Notebooks available in the project 

### initialNotebook 
This is the most basic first implementation. Has a lot of comments for a new user to understand what goes on in a RAG pipeline

### testingAlternatives and testingAlternatives2
These two files mimic what was done in the initialNotebook but is experimenting with different text-splitters, models, file-types etc

### onePrinterFile and multiplePrinterFiles
These are notebooks for a very specific usecase and a particular set of files that I wanted to test the model on. As the names suggest one uses only one pdf file while the latter uses 7-8 pdf files as a knowledge base for the RAG model

### holdingConversation and holdingConversationSelf
These are notebooks where there's no RAG, we are just trying to keep the LLMs chat history with us intact so that it can answer questions based on the previous conversation as well. The first file utilises langchain libraries while the latter is a more straight forward approach of keeping the chat history maintained

### ragWithConversation
Trying to integrate the RAG POC and the POCs for holding conversations with an LLM and trying to combine both to give a RAG which is capable of remembering it's conversation with the user 

