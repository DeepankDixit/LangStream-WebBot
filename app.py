#Chat with multiple Web URLs
import os
import time
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv
from bs4 import BeautifulSoup


os.environ["LANGCHAIN_TRACING_V2"]="true"

load_dotenv()

def get_vectorstore_from_url(urls):

    with st.sidebar:
        with st.spinner('Loading the document...'):
            # document loading
            loader = WebBaseLoader(urls)
            document = loader.load()
            # time.sleep(1)
        st.success('Document loaded!', icon="✅")
        # st.write(document[0])

    with st.sidebar:
        with st.spinner('Splitting the document into chunks...'):
            #document chunking
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=500)
            document_chunks = text_splitter.split_documents(document)
            # time.sleep(1)
        st.success(f'Document chunking completed! {len(document_chunks)} chunks', icon="✅")
        print(document_chunks)

    with st.sidebar:
        with st.spinner('Creating vectorstore from document chunks...'):
            #creating embeddings from documents and storing in vectorstore
            embeddings = OpenAIEmbeddings()
            vector_store = Chroma.from_documents(document_chunks, embeddings) #two args: 1: doc chunks, 2: embeddings
            # time.sleep(1)
        st.success('Embeddings created and saved to vectorstore', icon="✅")
        st.info("This vector store will take care of storing embedded data and perform vector search for you.")
        # st.write(vector_store)
    
    return vector_store

def get_context_retriever_chain(vector_store):
    llm = ChatOpenAI(temperature=0)

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    #Retrievers accept a string query as input and return a list of Document's as output, taken from the vectorstore. 
    #You can limit the number of documents in the returned list using db.as_retriever(search_kwargs={"k": 1}) 
    #default seems to be k = 4
    # create conversation chain

    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])

    retriever_chain = create_history_aware_retriever(
        llm=llm, 
        retriever=retriever,
        prompt=prompt
    )

    return retriever_chain

def get_conversational_rag_chain(retriever_chain):
    llm = ChatOpenAI(temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's question based on the below context:\n\n{context}."),
        ("system", "Also return the sources of your answer from the response metadata."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])

    #create_stuff_documents_chain takes a list of documents and formats them all into a prompt, then passes that prompt to an LLM. It passes ALL documents, so you should make sure it fits within the context window the LLM you are using.
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)

    #create_retrieval_chain takes in a user inquiry, which is then passed to the retriever to fetch relevant documents. Those documents (and original inputs) are then passed to an LLM to generate a response
    return create_retrieval_chain(retriever_chain, stuff_documents_chain)
    #create_retrieval_chain returns a dictionary containing at the very least a context and answer key.

def get_response(user_input):
    # create conversation chain
    retriever_chain = get_context_retriever_chain(st.session_state.vector_store)

    # call the conversational rag chain
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain) #to actually answer the user question

    response = conversation_rag_chain.invoke({
            "chat_history": st.session_state.chat_history,
            "input": user_query
        })
    
    return response['answer']
    return response #returns what create_retrieval_chain() returns


# app config
st.set_page_config(page_title="ISE Chat Assistant for URLs", page_icon="🔐") #what is going to show in the tab of your webpage
st.title("ISE Chat Assistant for URLs")

# sidebar
#when you use 'with' - anything inside of the sidebar, goes in here
with st.sidebar:
    st.header("Settings")
    option = st.selectbox(
        'Select number of URLs to chat with...',
        ('1', '2', '3', '4', '5')
    )
    urls = []
    if option is not None:
        for i in range(int(option)):
            url = st.text_input(f"URL {i+1}")
            urls.append(url)
        # website_url = st.text_input("Website URLs")


#if there is no website URL entered by the user, then let's disable the chat portion on the right 
if any(website_url is None or website_url == "" for website_url in urls):
    st.info("Please enter the website URLs")

else:
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello, I am a bot. How can I help you?")
        ]
    
    #build the vectorstore from website url
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = get_vectorstore_from_url(urls)

    #user input
    user_query = st.chat_input("Type your message here...")
    if user_query is not None and user_query != "":
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        # response = "placeholder response"
        response = get_response(user_query)
        # st.write(response)
        st.session_state.chat_history.append(AIMessage(content=response))

    # show the HumanMessage and AIMessage as conversation on the webpage
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)


