import requests
import json
import time

API_URL = "http://127.0.0.1:9090/chat"
HEADERS = {"Content-Type": "application/json"}
CUSTOMER_ID = "cust_12345"

TEST_CASES = [
    ("Hello", "Greeting"),
    ("How does the installment plan work?", "Policy - Installment Plan"),
    ("Where is my order?", "Order Status (Database)"),
    ("When is my next installment?", "Installment (Calculation)"),
    ("Where is my refund?", "Refund Status (Dummy Data)"),
    ("Connect me to customer care", "Human Handoff (New Intent)"),
    ("What is the weather today?", "Fallback (Professional)")
]

def run_tests():
    print(f"Running Demo Verification for User: {CUSTOMER_ID}\n")
    
    for message, scenario in TEST_CASES:
        payload = {
            "message": message,
            "customer_id": CUSTOMER_ID
        }
        
        try:
            print(f"--- Scenario: {scenario} ---")
            print(f"User: {message}")
            start = time.time()
            response = requests.post(API_URL, headers=HEADERS, json=payload)
            duration = time.time() - start
            
            if response.status_code == 200:
                print(f"Bot ({duration:.2f}s): {response.json().get('response')}")
            else:
                print(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Connection Error: {e}")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    time.sleep(2) # Wait for server to be fully ready
    run_tests()
