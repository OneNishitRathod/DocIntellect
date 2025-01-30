import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from config import VECTOR_STORE_PATH, DATA_PATH
import os
import shutil
import subprocess

# Load ChromaDB
embeddings = OllamaEmbeddings(model="deepseek-r1:8b")
vectorstore = Chroma(persist_directory=VECTOR_STORE_PATH, embedding_function=embeddings)
retriever = vectorstore.as_retriever()

# Chatbot
qa_chain = RetrievalQA.from_chain_type(
    llm=OllamaLLM(model="deepseek-r1:8b"),
    retriever=retriever,
)

# Streamlit UI
st.title("📄 AI Chatbot for Documents")

# File Upload Section
uploaded_file = st.file_uploader("Upload a document (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file:
    file_path = os.path.join(DATA_PATH, uploaded_file.name)
    
    # Save the file locally
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("Document uploaded successfully! Processing...")

    # Run ingestion script
    subprocess.run(["python", "ingest.py"])
    
    st.success("Document processed and added to the database!")

# Textbox for Querying
query = st.text_input("Ask something about your document:")
if query:
    response = qa_chain.invoke(query)
    st.write(response)