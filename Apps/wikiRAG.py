import streamlit as st
import time
import streamlit_analytics2 as streamlit_analytics
from urllib.parse import urlparse, unquote
import requests
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import TokenTextSplitter
import ollama
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate

# Initialize session state
if 'setup_complete' not in st.session_state:
    st.session_state['setup_complete'] = False
if 'documents' not in st.session_state:
    st.session_state['documents'] = None
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [('',''),('',''),('',''),('',''),('',''),('','')]
if 'url' not in st.session_state:
    st.session_state['url'] = ""
if 'query' not in st.session_state:
    st.session_state['query'] = ""
if 'retreiver' not in st.session_state:
    st.session_state['retreiver'] = None
if 'model' not in st.session_state:
    st.session_state['model'] = Ollama(model="llama3.1")

# Method for fetching the data in a wikipedia page using a wiki url
def getData(url):

    # Getting the title of the wiki page from the url
    path = urlparse(url).path
    title = unquote(path.split('/')[-1])

    # Calling the wikipedia api 
    endpoint = "https://en.wikipedia.org/w/api.php"
    params = {
        "action" : "query",
        "format" : "json",
        "titles" : title,
        "prop" : "extracts",
        "explaintext" : True
    }

    # Making the API call (Doesn't work on office laptop, ssl cert issue)
    #response = requests.get(endpoint, params = params, verify = False)        # For work laptop but this is security issue
    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    data = response.json()

    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    if "extract" in page:
        return page["extract"]
    else :
        return None

# Method for creating a vectorstore given a wikipedia url
def ingestDocument(url):
    data = getData(url)
    text_splitter = TokenTextSplitter(chunk_size=500,chunk_overlap=100)
    documents = text_splitter.split_text(data)
    docs = [Document(page_content=document, metadata={"source": "local"}) for document in documents]
    db = FAISS.from_documents(docs, OllamaEmbeddings(model = "nomic-embed-text"))
    retriever = db.as_retriever()
    return retriever     

# Utility for formatting fetched context 
def combineDocs(docs):
    context = "\n\n".join(f'Document Content : \n{doc.page_content} ]' for doc in docs)
    return context

#region Defining the prompt template
template = """
You are a helpful assistant. You are given some text, conversation history and a question. 
Answer the question based on the information given in the text or based on the conversation if needed

## Text ##
{context}

## Conversation ##
{conversation}
\n
Question : {question}
Answer: 

"""

prompt = PromptTemplate.from_template(template)

#endregion

# Method for getting last 3 questions and answers from chat history into a string 
def getChat():
    return "\nQuestion : " + st.session_state['chat_history'][-6][-1] + "\nAnswer : " + st.session_state['chat_history'][-5][-1] + "\nQuestion : " + st.session_state['chat_history'][-4][-1] + "\nAnswer : " + st.session_state['chat_history'][-3][-1] + "\nQuestion : " + st.session_state['chat_history'][-2][-1] + "\nAnswer : " + st.session_state['chat_history'][-1][-1]

# Method for calling the chat
def chat(question): 
    
    contextString = combineDocs(st.session_state['retreiver'].invoke(question))
    
    query = prompt.format(conversation = getChat(), context = contextString, question = question)
    
    response = st.session_state['model'].invoke(query)
    
    st.session_state['chat_history'].append(("User",question))
    st.session_state['chat_history'].append(("Assistant",response))

    return response


#region Streamlit app
st.title("Talk to Wikipedia")

st.markdown("""
1. Paste wiki link
2. Give the app some time to look at the document
3. Ask any question you want
""")

with streamlit_analytics.track():
    # URL input for document ingestion
    st.session_state['url'] = st.text_input("Enter URL to crawl and ingest the wiki document:", value=st.session_state['url'])
    
    # Combined Ingest and Setup button
    if st.button("Ingest and Setup"):
        with st.spinner("Setting up query engine..."):
            
            if st.session_state['url']:
                st.session_state['retreiver'] = ingestDocument(st.session_state['url'])
                st.success(f"Documents ingested from {st.session_state['url']} and query engine setup completed successfully!")
                st.session_state['setup_complete'] = True
            else:
                st.success(f"Please enter a url first")
            
    # Query input
    st.session_state['query'] = st.text_input("Enter your query:", value=st.session_state['query'])
    
    # Search button
    if st.button("Search"):
        if not st.session_state['setup_complete']:
            st.error("Please complete the setup first")
        elif st.session_state['query']:
            with st.spinner("Searching..."):
                try:
                    response = chat(st.session_state['query'])
                    pass
                except Exception as e:
                    st.error(f"Oops something went wrong. Error: {str(e)}")
                    st.stop()

            
            # Display the most recent response prominently
            st.subheader("Assistant's Response:")
            st.write(response)
        else:
            st.error("Please enter a query")
    
    # Sidebar for chat history
    st.sidebar.title("Chat History")
    for (user,message) in st.session_state['chat_history'][6:]:
        st.sidebar.text(f"{user}:{message}")
    
    # Clear chat history button in sidebar
    if st.sidebar.button("Clear Chat History"):
        st.session_state['chat_history'] = [('',''),('',''),('',''),('',''),('',''),('','')]
        st.sidebar.success("Chat history cleared!")

#endregion