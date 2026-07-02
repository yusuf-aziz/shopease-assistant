from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import logging
import uvicorn
import os
from pathlib import Path

from app.workflow.workflow import chat_graph

# --- Logging Setup ---
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# --- FastAPI App ---
app = FastAPI()

# --- CORS Middleware (for frontend to work) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Get absolute paths ---
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "frontend" / "static"
HTML_FILE = BASE_DIR / "frontend" / "index.html"

# --- Mount Static Files for Frontend ---
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# --- Models ---
class ChatRequest(BaseModel):
    message: str
    customer_id: str = None # Primary ID
    customer_mobile_no: str = None  # Deprecated but kept for backward compat
    store_wa_number: str = None
    session_id: str = None


# --- Frontend Route ---
@app.get("/")
async def read_root():
    """Serve the chatbot UI"""
    return FileResponse(str(HTML_FILE))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Server is running"}


# --- Chat Endpoint ---
@app.post("/chat")
def chat(req: ChatRequest):
    # Determine ID: explicit customer_id -> mobile -> session -> demo
    customer_id = req.customer_id or req.customer_mobile_no or req.session_id or "demo-user"

    logger.info(f"Request received: message='{req.message}' from {customer_id}")

    # Prepare state for workflow
    state = {
        "message": req.message,
        "customer_id": customer_id,
        "store_wa_number": req.store_wa_number or "demo-store-001"
    }

    # Call your workflow
    result = chat_graph.invoke(state)
    logger.debug(f"Workflow result: {result}")

    # Return response in format expected by frontend
    return {"response": result.get("response", "I'm sorry, I couldn't process that.")}


# --- Debug / Run Entry Point ---
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=9090,
        log_level="debug",
        access_log=True
    )