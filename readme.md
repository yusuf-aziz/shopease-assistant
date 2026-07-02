# ShopEase Assistant

A production-ready AI shopping assistant powered by RAG, agents and LangChain. It answers order/stock/refund/installment questions from real data, answers policy questions using RAG over your own documents, and supports both text and voice.

## How it works

1. **Route** — an LLM call classifies each message into an intent (`order_status`, `refund_status`, `installment_query`, `policy_query`, `human_handoff`, `general_chat`) using structured output, via a LangGraph state graph.
2. **Answer**
   - Order status, refund status and installments are looked up directly from a SQLite database — no LLM guessing involved.
   - Policy questions go through RAG: relevant chunks are retrieved from a Chroma vector store and the LLM answers using only that context.
3. **Voice** — the frontend uses the browser's Web Speech API for speech-to-text input and text-to-speech output, so you can talk to the assistant instead of typing.

## Tech stack

- FastAPI for the API
- LangGraph for intent routing
- LangChain + Groq (`llama-3.1-8b-instant`) for the LLM
- Chroma + `sentence-transformers/all-MiniLM-L6-v2` for RAG
- SQLAlchemy + SQLite for order data

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `app/.env` with your Groq API key:

```
GROQ_API_KEY=your-key-here
```

Load the demo data (orders + policy documents):

```bash
python -m app.script.load_store_data
```

## Run

```bash
uvicorn app.main:app --port 9090 --reload
```

Then open `http://localhost:9090` in your browser to chat (by typing or by voice).

## Project structure

```
app/
├── main.py              # FastAPI app and /chat endpoint
├── config.py             # LLM, DB and Chroma configuration
├── workflow/              # LangGraph intent-routing graph
├── llm/                   # Router and response-formatting prompts
├── service/                # Handlers: order/refund/installment, policy (RAG), fallback
├── dao/                    # SQLAlchemy models/session + Chroma vector store
├── models/                 # Order model
├── frontend/                # Chat UI with voice input/output
└── script/                  # Data loading and debug scripts
```
