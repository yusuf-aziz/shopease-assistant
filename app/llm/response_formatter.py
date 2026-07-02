from app.config import storesoffers_llm


def format_price_response_with_llm(docs, user_query):

    products_info = ""
    for i, doc in enumerate(docs, 1):
        md = doc.metadata
        products_info += f"""
            Product {i}:
            Name: {md['productName']}
            Price: {md['price']} AED
            Availability: {"In stock" if md['availability'] else "Out of stock"}
            Category: {md['category']}
            """

    prompt = f"""
                You are a helpful retail assistant.
                Use ONLY the verified data below.
                Do NOT change prices, availability, or invent details.
                
                User Query: {user_query}
                
                Products Data: {products_info}
                
                Rules:
                1. Only respond with products that clearly match the user query (by name or category).
                2. Deduplicate products by productName before responding.
                3. Respond in **short, friendly sentences**, one per product, like:
                   "Yes, we have <productName> for <price> AED, <availability>."
                4. If no products match, respond exactly:
                   "Sorry, I couldn’t find a relevant product for your request."
                5. Do NOT explain, reason, or add anything else.
                """
    response = storesoffers_llm.invoke(prompt)
    return response.content


def format_order_response_with_llm(orders, user_query):
    orders_info = ""

    for order in orders:
        orders_info += f"""
        Order ID: {order['order_id']}
        Products: {order['products']}
        Status: {order['status']}
        Placed on: {order['placed_on']}
        """

    prompt = f"""
        You are a helpful customer care assistant.
        Use ONLY the data exactly as provided.
        DO NOT paraphrase, infer, assume, or add explanations.
        DO NOT add apologies, reassurance, shipping info, or future updates.

        User Query: {user_query}

        Orders Data: {orders_info}

        Response Rules (STRICT):
        1. If Orders Data is present, output ONLY the order details.
        2. If the order status is PENDING, append this exact sentence after order or orders:
            "We are processing your order and will update you once it's ready."
        3. Use EXACTLY this format:
           Order ID: <Order ID>
           Products: <Products>
           Status: <Status>
           Placed on: <Placed on>
        4. If no orders exist, respond EXACTLY:
           No order found for you.
        5. Do NOT add anything else.
    """

    response = storesoffers_llm.invoke(prompt)
    return response.content
