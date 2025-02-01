# DocIntellect - AI-Powered Document Chatbot using RAG, LangChain, Chroma, and Ollama
DocIntellect is a powerful AI-driven application designed to interact with and extract insights from your documents, books, or files. By leveraging **Retrieval-Augmented Generation (RAG)**, it combines a powerful large language model with a vector-based document retrieval system to provide precise and context-aware answers based on your data.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [License](#license)

## Features

- **Document Ingestion**: Process PDFs and text files to create searchable embeddings.
- **Retrieval-Augmented Generation (RAG)**: Combines vector retrieval with LLM generation to answer queries with relevant context.
- **Interactive Web Interface**: Built with Streamlit for a responsive, user-friendly chat interface.
- **Chroma Vector Store**: Uses Chroma Database for efficient storage and retrieval of document embeddings.
- **Ollama Integration**: Utilizes the DeepSeek R1 8B model (via Ollama) as the language model to generate responses.

## Technologies Used

- **Programming Language**: Python 3.12.8
- **Web Framework**: [Streamlit](https://streamlit.io/)
- **RAG Framework & Document Processing**: [LangChain](https://github.com/langchain-ai/langchain)
- **Language Model Interface**: [Ollama](https://ollama.com/)
  - **DeepSeek R1 8B Model**: Used as the LLM for generating responses.
- **Vector Database**: [Chroma](https://www.trychroma.com/)
- **Document Loaders**: 
  - `PyPDFLoader` for PDFs
  - `TextLoader` for plain text files
- **Document Splitting**: `RecursiveCharacterTextSplitter` from LangChain

# Installation

## 1. Clone the Repository
  ```bash
  git clone https://github.com/onenishitrathod/DocIntellect.git
  cd DocIntellect
  ```

## Project Structure
```plaintext
DocIntellect/
│── app.py                # Main Streamlit web app
│── ingest.py             # Script to process and store document embeddings in Chroma DB
│── config.py             # Configuration settings
│── utils.py              # Helper functions for document processing
│── requirements.txt      # Python dependencies
│── data/                 # Directory for document files (PDFs, TXT, etc.)
│── chroma_db/            # Directory for storing the Chroma database
│── README.md             # Project documentation
```

## 2. Create and Activate a Virtual Environment
  ```bash
  python -m venv venv
  On Windows: venv\Scripts\activate
  On macOS/Linux: source venv/bin/activate
  ```

## 3. Install the Dependencies
  ```bash
  pip install -r requirements.txt
  ```

## 4. Install Ollama and Pull the deepseek-r1:8b model
  ```bash
  [Ollama](https://ollama.com/)
  ollama --version
  ollama pull deepseek-r1:8b
  ```
Note: If you prefer using WSL (Windows Subsystem for Linux), you can install Ollama using the shell script as described on their website.

## 5. Process Your Documents
  ```bash
  python ingest.py
  ```
This will load your documents, split them into manageable chunks, generate embeddings using Ollama, and store them in the Chroma vector database located in the vectorstore/ directory.

## 6. Usage
  ```bash
streamlit run app.py
  ```
Open your browser and navigate to the local URL provided by Streamlit. You can then enter questions related to your documents, and the chatbot will retrieve and display the relevant information.
