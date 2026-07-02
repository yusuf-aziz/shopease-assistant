from app.config import storesoffers_llm
from app.dao.core.chroma import vectorstore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Initialize RAG Prompt
RAG_PROMPT = """
You are a friendly and helpful customer support agent for ShopEase, an online store.
Your goal is to assist users with their questions warmly and professionally.

Answer the user's question about our policies based ONLY on the following context.
- Use a polite and conversational tone (e.g., "I'd be happy to explain...", "Here is what you need to know about...").
- Keep the answer concise but helpful.
- If the answer is not in the context, say "I'm sorry, but I couldn't find that specific information in my records. Please reach out to our support team for further assistance."

Context:
{context}

User Question: {message}
"""

def retrieve_context(query):
    # Retrieve top 2 most relevant policy chunks
    results = vectorstore.similarity_search(query, k=2)
    return "\n\n".join([doc.page_content for doc in results])

def policy_handler(state):
    message = state["message"]
    
    # Simple RAG Chain
    context = retrieve_context(message)
    
    prompt = ChatPromptTemplate.from_template(RAG_PROMPT)
    chain = prompt | storesoffers_llm
    
    response = chain.invoke({"context": context, "message": message})
    state["response"] = response.content
    return state
