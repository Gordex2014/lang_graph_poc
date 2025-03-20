from langchain_core.messages import SystemMessage, HumanMessage
from api.fhir_api import FhirApi
from llm.get_chat import get_chat
from state.state import PromptState, add_requested_resource


def get_requested_resource(state: PromptState) -> PromptState:
    if not state['user_question']:
        raise ValueError("Requested resource is not set in the state")
    
    resources_list = None
    
    try:
        fhir_api = FhirApi()
        resources = fhir_api.authenticated_request("http://localhost:8181/fhir/resources")
        # Filter out resources with state 'INACTIVE' and extract their supportedResource
        supported_resources = [
            resource.get('supportedResource') 
            for resource in resources if resource.get('state') != "INACTIVE"
        ]
        resources_list = ", ".join(supported_resources)
    except Exception as e:
        print(f"Error: {e}")
        raise ValueError("Failed to authenticate with FHIR server")
    
    llm = get_chat()
    
    sys_prompt = f"You are a FHIR expert using the r4 version of the standard. You are going to be asked questions about the following resources: {resources_list}"
    human_prompt = f"Based on the following question, which single FHIR resource is involved? Please just give me the more likely to be involved and discard the other ones. Here is the question: {state['user_question']}. Don't give any explanation about your choice, just return the resource name. If you have to choose between diagnostic reports and observation, always pick observation. If the question I am asking has nothing to do with FHIR, just say 'I don't know' and don't give any explanation."
    
    sys_message = SystemMessage(sys_prompt)
    human_message = HumanMessage(human_prompt)
    
    result = llm.invoke([sys_message, human_message])
    
    if (
        not result or
        not result.content or
        not isinstance(result.content, str) or
        result.content == "I don't know"
    ):
        raise ValueError("Unrelated questions, please ask a question related to FHIR resources")
    
    print(f"Requested resource: {result.content}")
    return add_requested_resource(state, result.content)
    