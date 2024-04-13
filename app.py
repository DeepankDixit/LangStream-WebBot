import streamlit as st 
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma #all 3rd party integrations come under langchain_community package
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv

load_dotenv()

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

def get_vectorstore_from_url(url):
    # get the text in document form
    loader = WebBaseLoader(url)
    document = loader.load()

    #split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(document)
    
    #create a vectorstore from chunks 
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(document_chunks, embeddings) #two args: 1: doc chunks, 2: embeddings

    return vector_store

def get_context_retriever_chain(vector_store):
    llm = ChatOpenAI()

    retriever = vector_store.as_retriever()

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
    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's question based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])

    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)

    return create_retrieval_chain(retriever_chain, stuff_documents_chain)

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


# app config
st.set_page_config(page_title="Chat with websites", page_icon="🤖") #what is going to show in the tab of your webpage
st.title("Chat with websites")

# sidebar
#when you use 'with' - anything inside of the sidebar, goes in here
with st.sidebar:
    st.header("Settings")
    website_url = st.text_input("Website URL")

#if there is no website URL entered by the user, then let's disable the chat portion on the right
if website_url is None or website_url == "":
    st.info("Please enter a website URL")

else:
    # session state
    #session state object/var doesn'y change everytime the code is reloaded due to app activity in streamlit
    #AIMessage and HumanMessage- std schemas offered in LangChain
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello, I am your assistant. How can I help you?"),
        ]
    
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = get_vectorstore_from_url(website_url)

    # user input
    #create an input bar for your dialogues
    user_query = st.chat_input("Type your message here...")
    if user_query is not None and user_query != "":
        response = get_response(user_query)
        st.write(response)
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=response))

        
    # with st.sidebar:
    #     st.write(st.session_state.chat_history)

    # conversation
    #looping through all of the elems inside of the chat_history, which is stored in a session state var
    for message in st.session_state.chat_history: 
        if isinstance(message, AIMessage): #if the message is in instance of an AIMessage
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage): #if the message is in instance of an HumanMessage
            with st.chat_message("Human"):
                st.write(message.content)




