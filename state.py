from typing import TypedDict, Annotated, List, Any
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    user_message: str
    intent: str
    response: str
    history: Annotated[List[BaseMessage], add_messages]