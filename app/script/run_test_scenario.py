import requests
import sys
import time

API_URL = "http://127.0.0.1:9090/chat"
HEADERS = {"Content-Type": "application/json"}

# Demo Scenarios
TEST_CASES = [
    ("Hello", "Greeting"),
    ("How does the installment plan work?", "Policy - Installment Plan"),
    ("Where is my order?", "Order Status (Database)"),
    ("When is my next installment?", "Installment (Calculation)"),
    ("Where is my refund?", "Refund Status (Differs by User)"),
    ("Connect me to customer care", "Human Handoff")
]

def run_demo(user_id):
    print(f"\n🚀 Running Demo for User: {user_id}")
    print("="*60)
    
    for message, scenario in TEST_CASES:
        payload = {
            "message": message,
            "customer_id": user_id
        }
        
        try:
            print(f"\n🔹 Scenario: {scenario}")
            print(f"User: {message}")
            start = time.time()
            response = requests.post(API_URL, headers=HEADERS, json=payload)
            duration = time.time() - start
            
            if response.status_code == 200:
                bot_reply = response.json().get('response')
                print(f"Bot ({duration:.2f}s): {bot_reply}")
            else:
                print(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Connection Error: {e}")
            break
        
        time.sleep(0.5)

    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    
    user_id = sys.argv[1]
    run_demo(user_id)
