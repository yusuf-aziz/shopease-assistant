from langgraph.graph import StateGraph

from app.service.fallback_service import fallback_handler
from app.service.store_service import order_status_handler, refund_status_handler, installment_handler, human_handoff_handler
from app.service.policy_service import policy_handler
from app.llm.router import router_llm, ROUTER_PROMPT


def router_node(state):
    result = router_llm.invoke(
        ROUTER_PROMPT.format(message=state["message"])
    )

    state["intent"] = result.intent
    # state["entities"] = result.dict() # removed as we simplified the schema

    print(f'state : {state}')
    return state


def route(state):
    return state["intent"]


graph = StateGraph(dict)

graph.add_node("router", router_node)
graph.add_node("policy", policy_handler)
graph.add_node("order_status", order_status_handler)
graph.add_node("refund_status", refund_status_handler)
graph.add_node("installment", installment_handler)
graph.add_node("human_handoff", human_handoff_handler)
graph.add_node("fallback", fallback_handler)

graph.set_entry_point("router")

graph.add_conditional_edges(
    "router",
    route,
    {
        "policy_query": "policy",
        "order_status": "order_status",
        "refund_status": "refund_status",
        "installment_query": "installment",
        "human_handoff": "human_handoff",
        "general_chat": "fallback"
    }
)

chat_graph = graph.compile()
