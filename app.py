import os
import streamlit as st
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from config import VECTOR_STORE_PATH, DATA_PATH
from utils import load_documents, process_documents

# ------------------------------
# Aesthetic CSS for Chat Bubbles
# ------------------------------
st.markdown(
    """
    <style>
    .chat-container {
        max-width: 800px;
        margin: auto;
    }
    .user-message {
        background-color: #DCF8C6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: right;
        word-wrap: break-word;
    }
    .assistant-message {
        background-color: #F1F0F0;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: left;
        word-wrap: break-word;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------
# Function to ingest documents into ChromaDB
# --------------------------------------------
def ingest_documents():
    # Load and process documents from the DATA_PATH directory
    docs = load_documents(DATA_PATH)
    split_docs = process_documents(docs)
    
    # Create and persist the vector database
    embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b")
    vectorstore = Chroma(persist_directory=VECTOR_STORE_PATH, embedding_function=embeddings)
    vectorstore.add_documents(split_docs)
    return vectorstore

# ---------------------------------------------------
# Initialize embeddings, vectorstore, retriever, & QA
# ---------------------------------------------------
embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b")
vectorstore = Chroma(persist_directory=VECTOR_STORE_PATH, embedding_function=embeddings)
retriever = vectorstore.as_retriever()

qa_chain = RetrievalQA.from_chain_type(
    llm=OllamaLLM(model="deepseek-r1:1.5b"),
    retriever=retriever,
)

# ------------------------------------------------
# Initialize session state to hold conversation
# ------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --------------------
# App Title and Header
# --------------------
st.title("📄 AI Chatbot for Documents")

# ---------------------------
# File Upload & Ingestion Block
# ---------------------------
uploaded_file = st.file_uploader("Upload a document (PDF or TXT)", type=["pdf", "txt"])
if uploaded_file:
    file_path = os.path.join(DATA_PATH, uploaded_file.name)
    
    # Save the file locally
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Process the document and update the vectorstore
    vectorstore = ingest_documents()
    
    # Update the retriever and QA chain with the new vectorstore
    retriever = vectorstore.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=OllamaLLM(model="deepseek-r1:1.5b"),
        retriever=retriever,
    )
    
    st.success("Ask your question or look at right-top till it says Running...")

# ------------------------------
# Display the Chat Conversation
# ------------------------------
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for chat in st.session_state.chat_history:
        role = chat["role"]
        content = chat["content"]
        # Use different styling for user and assistant messages
        if role == "user":
            st.markdown(f'<div class="user-message">{content}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message">{content}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------
# Chat Input Form Block
# ---------------------
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message:")
    submit_button = st.form_submit_button(label="Send")
    
    if submit_button and user_input:
        # Get the raw response from the QA chain
        raw_response = qa_chain.invoke(user_input)
        
        # Format the output if it is a dictionary with "query" and "result"
        if isinstance(raw_response, dict) and "query" in raw_response and "result" in raw_response:
            query_text = raw_response.get("query", "")
            result_text = raw_response.get("result", "")
            formatted_response = (
                f"### Query:\n{query_text}\n\n"
                f"### Response:\n{result_text}"
            )
        else:
            # Otherwise, use the raw response as-is.
            formatted_response = raw_response
        
        # Append the user input and formatted response to the chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": formatted_response})
        
        # Rerun the app to refresh the conversation display
        st.rerun()
