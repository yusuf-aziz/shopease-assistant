import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from sqlalchemy import create_engine, text
from app.config import DB_PATH

def check_db():
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at: {DB_PATH}")
        return

    print(f"✅ Database found at: {DB_PATH}")
    engine = create_engine(f"sqlite:///{DB_PATH}")
    
    with engine.connect() as conn:
        print("\n--- Checking Orders Table ---")
        result = conn.execute(text("SELECT order_id, customer_id, store_id FROM orders"))
        rows = result.fetchall()
        
        if not rows:
            print("⚠️ Orders table is empty!")
        else:
            for row in rows:
                print(f"Order: {row[0]} | Customer: {row[1]} | Store: {row[2]}")

if __name__ == "__main__":
    check_db()
