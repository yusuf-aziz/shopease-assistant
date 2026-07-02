import sys
import os

# Ensure app modules can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.dao.core.chroma import vectorstore
from langchain_chroma import Chroma
from app.config import CHROMA_PATH
from langchain_huggingface import HuggingFaceEmbeddings
from app.dao.order_dao import save_order
from app.models.order import OrderStatusEnum
from datetime import datetime

def load_policy_data():
    print("Loading Policy Data into Chroma...")
    # Initialize Embedding
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Initialize VectorStore (clearing old data)
    try:
        vectorstore = Chroma(
            collection_name="store_policies", # New collection for policies
            embedding_function=embedding,
            persist_directory=CHROMA_PATH
        )
        vectorstore.delete_collection()
    except:
        pass

    # Re-initialize after deletion (or fresh create)
    vectorstore = Chroma(
        collection_name="store_policies",
        embedding_function=embedding,
        persist_directory=CHROMA_PATH
    )

    policies = [
        {
            "content": "ShopEase's installment plan lets you split your purchase into interest-free payments. You pay a portion today, and the rest is spread over automatic monthly payments. There are no interest charges or hidden fees if you pay on time.",
            "metadata": {"topic": "installment_plan_explanation", "source": "how_it_works"}
        },
        {
            "content": "Our refund policy is simple: Returns are processed within 5-7 business days after the merchant receives the item. Once processed, the refund amount is credited back to your original payment method.",
            "metadata": {"topic": "refund_timeline", "source": "policy_faq"}
        },
        {
            "content": "If you miss a payment, a late fee of 25 AED applies. We will send you reminders before the due date to help you avoid this.",
            "metadata": {"topic": "late_fees", "source": "terms"}
        },
        {
            "content": "You can contact ShopEase support via email at support@storesoffers.com, through the in-app chat 24/7, or by requesting to speak to a human agent here.",
            "metadata": {"topic": "contact_support", "source": "contact_info"}
        },
        {
             "content": "To return an item, please check the merchant's return policy first. Once the return is initiated with them, we will pause your installments until the refund is confirmed.",
             "metadata": {"topic": "how_to_return", "source": "faq"}
        }
    ]

    vectorstore.add_texts(
        texts=[p["content"] for p in policies],
        metadatas=[p["metadata"] for p in policies]
    )
    print("Policy Data loaded.")

from app.dao.core.session import engine
from app.dao.core.base import Base

def load_order_data():
    print("Loading Order Data into SQLite...")
    
    # Clean up old tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # --- User 1: 3001002402 (Active Refunds & High Value Orders) ---
    # Has matching refunds in store_service.py
    
    # Order 1: High value electronics (Pending)
    items_1 = [{"product": "MacBook Air", "price": 3500}, {"product": "AppleCare", "price": 500}]
    installments_1 = [
        {"due_date": "2026-02-01", "amount": 1333.33, "status": "PAID"}, # DP
        {"due_date": "2026-03-01", "amount": 1333.33, "status": "PENDING"},
        {"due_date": "2026-04-01", "amount": 1333.34, "status": "PENDING"}
    ]
    save_order(items_1, store_id="Apple Store", customer_id="3001002402", total_amount=4000.0, paid_amount=1333.33, installments=installments_1, next_due_date=datetime.strptime("2026-03-01", "%Y-%m-%d"))

    # Order 2: Returned Item (Relates to REF-9901)
    items_2 = [{"product": "Zara Jacket", "price": 450}]
    installments_2 = [
        {"due_date": "2026-01-10", "amount": 150.0, "status": "PAID"},
        {"due_date": "2026-02-10", "amount": 150.0, "status": "PAID"}, # Paid off before return processed?
        {"due_date": "2026-03-10", "amount": 150.0, "status": "PAID"}
    ]
    save_order(items_2, store_id="Zara", customer_id="3001002402", total_amount=450.0, paid_amount=450.0, installments=installments_2, next_due_date=None)

    
    # --- User 2: 3001002405 (No Refunds, Regular Spender) ---
    
    # Order 3: Adidas Sneakers (Active)
    items_3 = [{"product": "Yeezy Boost", "price": 900}]
    installments_3 = [
        {"due_date": "2026-02-05", "amount": 300.0, "status": "PAID"},
        {"due_date": "2026-03-05", "amount": 300.0, "status": "PENDING"},
        {"due_date": "2026-04-05", "amount": 300.0, "status": "PENDING"}
    ]
    save_order(items_3, store_id="Adidas", customer_id="3001002405", total_amount=900.0, paid_amount=300.0, installments=installments_3, next_due_date=datetime.strptime("2026-03-05", "%Y-%m-%d"))

    # Order 4: Small Purchase (Completed)
    items_4 = [{"product": "Coffee Machine", "price": 200}]
    installments_4 = [
        {"due_date": "2026-01-01", "amount": 66.66, "status": "PAID"},
        {"due_date": "2026-02-01", "amount": 66.66, "status": "PAID"},
        {"due_date": "2026-03-01", "amount": 66.68, "status": "PAID"}
    ]
    save_order(items_4, store_id="Noon", customer_id="3001002405", total_amount=200.0, paid_amount=200.0, installments=installments_4, next_due_date=None)
    
    print("Order Data loaded.")

if __name__ == "__main__":
    load_policy_data()
    load_order_data()
    print("Data Loading Complete.")
