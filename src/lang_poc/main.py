from langgraph.graph import StateGraph, START, END

from edges.check_view_definition import check_view_definition
from nodes.get_requested_resource import get_requested_resource
from nodes.get_user_question import get_user_question
from nodes.get_view_definition import get_view_definition
from nodes.handle_view_definition import handle_view_definition
from state.state import PromptState

# Build graph
builder = StateGraph(PromptState)
builder.add_node("get_user_question", get_user_question)
builder.add_node("get_requested_resource", get_requested_resource)
builder.add_node("get_view_definition", get_view_definition)
builder.add_node("handle_view_definition", handle_view_definition)
builder.add_edge(START, "get_user_question")
builder.add_edge("get_user_question", "get_requested_resource")
builder.add_edge("get_requested_resource", "get_view_definition")
builder.add_conditional_edges("get_view_definition", check_view_definition)
builder.add_edge("handle_view_definition", END)
graph = builder.compile()

state = graph.invoke({"user_question": "What is John Smith's latest blood pressure?", "requested_resource": None, "view_definition": None, "should_retry": False, "retry_count": 0})
