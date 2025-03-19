from typing import TypedDict

class PromptState(TypedDict):
    user_question: str
    requested_resource: str
    view_definition: str
    should_retry: bool
    retry_count: int
    
def add_user_question(state: PromptState, user_question: str) -> PromptState:
    return {
        'user_question': user_question,
        'requested_resource': state['requested_resource'],
        'view_definition': state['view_definition'],
        'should_retry': state['should_retry'],
        'retry_count': state['retry_count'],
    }
    
def add_requested_resource(state: PromptState, requested_resource: str) -> PromptState:
    return {
        'requested_resource': requested_resource,
        'user_question': state['user_question'],
        'view_definition': state['view_definition'],
        'should_retry': state['should_retry'],
        'retry_count': state['retry_count'],
    }
    
def add_view_definition(state: PromptState, view_definition: str) -> PromptState:
    return {
        'view_definition': view_definition,
        'user_question': state['user_question'],
        'requested_resource': state['requested_resource'],
        'should_retry': state['should_retry'],
        'retry_count': state['retry_count'],
    }
    
def commit_retry(state: PromptState) -> PromptState:
    return {
        'should_retry': True,
        'user_question': state['user_question'],
        'requested_resource': state['requested_resource'],
        'view_definition': state['view_definition'],
        'retry_count': state['retry_count'] + 1,
    }

def stop_retry(state: PromptState) -> PromptState:
    return {
        'should_retry': False,
        'user_question': state['user_question'],
        'requested_resource': state['requested_resource'],
        'view_definition': state['view_definition'],
        'retry_count': state['retry_count'],
    }
    
def unmodified(state: PromptState) -> PromptState:
    return {
        'should_retry': state['should_retry'],
        'user_question': state['user_question'],
        'requested_resource': state['requested_resource'],
        'view_definition': state['view_definition'],
        'retry_count': state['retry_count'],
    }
    