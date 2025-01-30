import os

# Configurations for VectorDB
VECTOR_STORE_PATH = "./chroma_db/"
DATA_PATH = "./data/"
MODEL_NAME = "deepseek-r1:8b"

# Ensure directories exist
os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
os.makedirs(DATA_PATH, exist_ok=True)
