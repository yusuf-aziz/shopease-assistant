from typing import List, Optional
from pydantic import BaseModel
from app.config import storesoffers_llm


class IntentSchema(BaseModel):
    intent: str
    customerId: Optional[str] = None


router_llm = storesoffers_llm.with_structured_output(IntentSchema)

ROUTER_PROMPT = """
                You are an intent router for ShopEase, an online store.
                
                Allowed intents:
                - policy_query (e.g., "what is the refund policy", "how does the installment plan work", "late fees", "missed payment", "how to return")
                - order_status (e.g., "where is my order", "status of order", "track order")
                - refund_status (e.g., "status of my return", "where is my refund", "check refund status")
                - installment_query (e.g., "when is my next installment", "how many installments remaining", "how much did I pay", "payment schedule")
                - human_handoff (e.g., "connect me to customer care", "i want to speak to a human", "talk to support")
                - general_chat (e.g., "hello", "thanks", "hi")
                
                Extract intent.
                
                User message:
                {message}
                """
