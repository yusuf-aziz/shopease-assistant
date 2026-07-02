from app.dao.order_dao import get_orders_by_customer

# Dummy Refunds (keyed by customer_id)
DUMMY_REFUNDS = {
    "3001002402": [
        {"id": "REF-9901", "order_id": "ORD-101", "amount": 450, "status": "Processed", "date": "2026-01-15"},
        {"id": "REF-9902", "order_id": "ORD-103", "amount": 120, "status": "Pending Merchant Approval", "date": "2026-02-01"}
    ],
    # 3001002405 has NO refunds (empty list by default)
}

def get_customer_id(state):
    # Retrieve customer_id from state, fallback to demo-user
    return state.get("customer_id") or "demo-user"

def order_status_handler(state):
    customer_id = get_customer_id(state)
    orders = get_orders_by_customer(customer_id)
    
    if not orders:
        state["response"] = "I couldn't find any recent orders for you. Detailed records are available in your ShopEase account."
    else:
        response_lines = ["I found these recent orders for you:"]
        for order in orders:
            total_amount = sum(item.get("price", 0) for item in order.items)
            # products = ", ".join(item.get("product", "Unknown") for item in order.items)
            # Simplify product listing to just the first item + count if more
            items = order.items
            first_product = items[0].get("product", "Item")
            product_display = f"{first_product} +{len(items)-1} more" if len(items) > 1 else first_product
            
            status = order.order_status.value if hasattr(order.order_status, "value") else str(order.order_status)
            
            response_lines.append(f"📦 **{product_display}**\n   ID: {order.order_id} | {total_amount} AED | {status}")
            
        response_lines.append("\nNeed help with a specific one?")
        state["response"] = "\n".join(response_lines)
    
    return state

def refund_status_handler(state):
    customer_id = get_customer_id(state)
    refunds = DUMMY_REFUNDS.get(customer_id, [])
    
    if not refunds:
         state["response"] = "I don't see any active refund requests right now. If you just requested one, give it a moment to update."
    else:
        response_lines = ["Here is the status of your refunds:"]
        for refund in refunds:
            response_lines.append(f"💸 **Refund for Order {refund['order_id']}**\n   {refund['amount']} AED • **{refund['status']}**\n   (Updated: {refund['date']})")
        
        response_lines.append("\nAnything else I can check for you?")
        state["response"] = "\n".join(response_lines)
        
    return state

def installment_handler(state):
    customer_id = get_customer_id(state)
    orders = get_orders_by_customer(customer_id)
    
    if not orders:
        state["response"] = "I couldn't find any active installment plans linked to your account."
        return state

    response_lines = []
    active_plans_found = False
    
    for order in orders:
        if not order.installments:
            continue
            
        installments = order.installments
        pending = [ins for ins in installments if ins['status'] == 'PENDING']
        paid = [ins for ins in installments if ins['status'] == 'PAID']
        
        if not pending and not paid:
             continue
             
        active_plans_found = True
        items = order.items
        first_product = items[0].get("product", "Item")
        product_display = f"{first_product}..." if len(items) > 1 else first_product
        
        response_lines.append(f"🗓️ **Plan: {product_display}**")
        response_lines.append(f"   Paid: {order.paid_amount} / {order.total_amount} AED")
        
        if pending:
            next_inst = pending[0]
            # Format date to be friendlier e.g. "05 Feb"
            try:
                due_dt = datetime.strptime(next_inst['due_date'], "%Y-%m-%d")
                friendly_date = due_dt.strftime("%d %b")
            except:
                friendly_date = next_inst['due_date']
                
            response_lines.append(f"   👉 **Next Pay:** {next_inst['amount']} AED on **{friendly_date}**")
        else:
            response_lines.append(f"   🎉 **All paid off!**")
        
        response_lines.append("") 

    if not active_plans_found:
        state["response"] = "You have no active payments due. You're all clear! ✨"
    else:
        response_lines.insert(0, "Here's a quick look at your payments:")
        response_lines.append("Want to make a payment now?")
        state["response"] = "\n".join(response_lines)
    
    return state

def human_handoff_handler(state):
    state["response"] = "No problem. I'm connecting you to a human agent now... 📞\n\nSomeone from the team will be with you in just a moment."
    return state
