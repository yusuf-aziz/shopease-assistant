import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Databases folder
DB_FOLDER = os.path.join(os.path.dirname(__file__), "databases")
os.makedirs(DB_FOLDER, exist_ok=True)

# SQLite paths
DB_PATH = os.path.join(DB_FOLDER, "shop.db")
CHROMA_PATH = os.path.join(DB_FOLDER, "chroma_db")

# LLM API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the environment!")

storesoffers_llm = ChatGroq(model="llama-3.1-8b-instant")
