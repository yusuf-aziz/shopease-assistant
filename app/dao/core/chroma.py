from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import CHROMA_PATH

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# This reloads the collection from disk if it exists
vectorstore = Chroma(
    collection_name="store_policies",
    embedding_function=embedding,
    persist_directory=CHROMA_PATH
)
