def fallback_handler(state):
    message = state.get("message", "").lower()
    
    greetings = ["hello", "hi", "hey", "good morning", "good afternoon"]
    if any(greet in message for greet in greetings):
        customer_id = state.get("customer_id")
        name = ""
        if customer_id == "3001002402":
            name = " Yusuf"
        elif customer_id == "3001002405":
            name = " Asad"
            
        state["response"] = f"Hello{name}! 👋 I'm your ShopEase assistant. How can I help you today? You can ask me about your orders, installments, refunds, or our policies."
    else:
        state["response"] = "I am specialized in assisting with your ShopEase orders. While I may not have the answer to that, I'd be happy to help with your installment plans, refund status, or our policies. How can I assist you?"
    
    return state
