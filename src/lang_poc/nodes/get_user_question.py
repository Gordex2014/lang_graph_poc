from state.state import PromptState, add_user_question

def get_user_question(state: PromptState) -> PromptState:
    if not state['user_question']:
        raise ValueError("User question is not set in the state")
    print(f"User question: {state['user_question']}")
    return add_user_question(state, state['user_question'])