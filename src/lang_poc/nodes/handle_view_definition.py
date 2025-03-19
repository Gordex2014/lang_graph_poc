from state.state import PromptState, unmodified


def handle_view_definition(state: PromptState) -> PromptState:
    # TODO: Implement this function
    print('View definition:')
    print()
    print(state['view_definition'])
    return unmodified(state)
