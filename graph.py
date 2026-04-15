from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

from Chatbot_simples.state import AgentState
from Chatbot_simples.nodes import classify_node, faq_node, response_node, fallback_node, update_history_node

def route(state):
    intent = state.get("intent", "")
    if intent == "faq":
        return "faq"
    elif intent in ["saudacao", "suporte", "novo"]:
        return "response"
    else:
        return "fallback"

def build_graph(checkpointer=None):
    """Constrói o grafo com suporte a checkpointer (persistência)."""
    graph = StateGraph(AgentState)

    graph.add_node("classify", classify_node)
    graph.add_node("faq", faq_node)
    graph.add_node("response", response_node)
    graph.add_node("fallback", fallback_node)
    graph.add_node("update_history", update_history_node)

    graph.add_edge(START, "classify")

    graph.add_conditional_edges(
        "classify",
        route,
        {
            "faq": "faq",
            "response": "response",
            "fallback": "fallback"
        }
    )

    graph.add_edge("faq", "update_history")           # FAQ → resposta final (caso precise)
    graph.add_edge("response", "update_history")
    graph.add_edge("fallback", "update_history")
    graph.add_edge("update_history", END)

    # Compila com checkpointer----------
    return graph.compile(checkpointer=checkpointer)
