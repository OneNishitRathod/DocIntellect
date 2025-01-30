from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

# Load documents
def load_documents(data_path):
    docs = []
    for file in os.listdir(data_path):
        file_path = os.path.join(data_path, file)
        if file.endswith(".pdf"):
            docs.extend(PyPDFLoader(file_path).load())
        elif file.endswith(".txt"):
            docs.extend(TextLoader(file_path).load())
    return docs

# Split and embed documents
def process_documents(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return text_splitter.split_documents(docs)
