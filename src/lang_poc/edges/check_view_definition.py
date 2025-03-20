from typing import Literal
from state.state import PromptState

def check_view_definition(state: PromptState) -> Literal["get_view_definition", "handle_view_definition"]:
    if state["should_retry"] is True:
        return "get_view_definition"
    
    if not state["view_definition"]:
        raise ValueError("View definition is not set in the state")
    
    return "handle_view_definition"
