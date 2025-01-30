from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from utils import load_documents, process_documents
from config import VECTOR_STORE_PATH, DATA_PATH

# Load and process documents
docs = load_documents(DATA_PATH)
split_docs = process_documents(docs)

# Create and persist vector DB
embeddings = OllamaEmbeddings(model="deepseek-r1:8b")
vectorstore = Chroma(persist_directory=VECTOR_STORE_PATH, embedding_function=embeddings)
vectorstore.add_documents(split_docs)

print("Documents processed and stored successfully in ChromaDB!")
