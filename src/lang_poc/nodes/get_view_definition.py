import re
import json
import requests

from constants.fhir_api import SQL_ON_FHIR_API_URL
from constants.retry import MAX_RETRY_COUNT
from llm.get_chat import get_chat
from state.state import PromptState, add_view_definition, commit_retry
from utils.get_html_as_text import get_html_as_text

def get_view_definition(state: PromptState) -> PromptState:
    if not state['user_question']:
        raise ValueError("User question is not set in the state")
    if not state['requested_resource']:
        raise ValueError("Requested resource is not set in the state")
    if state['should_retry'] is True and state['retry_count'] > MAX_RETRY_COUNT:
        raise ValueError("Retry limit exceeded, invalid view definition")
    
    sql_on_fhir_url = "https://build.fhir.org/ig/FHIR/sql-on-fhir-v2/StructureDefinition-ViewDefinition.html"
    curated_resource = state['requested_resource'].lower().replace(" ", "-")
    fhir_resource_docs_url = f"https://build.fhir.org/{curated_resource}.html"
    
    sql_on_fhir_text = get_html_as_text(sql_on_fhir_url)
    fhir_resource_docs_text = get_html_as_text(fhir_resource_docs_url)
    
    system_message = f"""You are a FHIR expert and you have all the required knowledge about
    sql-on-fhir and the {state['requested_resource']} resource. You are going to be asked questions about the
    {state['requested_resource']} resource and the sql-on-fhir standard.

    You are also supplied with the view definition documentation from the sql-on-fhir documentation here:
    {sql_on_fhir_text}.

    Also you have the {state['requested_resource']} resource documentation here:
    {fhir_resource_docs_text}.
    """

    human_message = (
        f"For this resource: {state['requested_resource']} and my question: {state['user_question']}. "
        "Please provide a view definition that can be used to query the resource. The view definition "
        "should be based on the sql-on-fhir standard, don't give any sort of explanation or "
        "annotation, just the view definition in JSON format."
    )
    
    llm = get_chat()
    result = llm.invoke([system_message, human_message])
    new_view_definition = None
    
    # Validate the content
    try:
        # Remove "```json" from the start and "```" from the end of the content.
        result.content = re.sub(r'^```json', '', result.content)
        result.content = re.sub(r'```$', '', result.content)
        # Validate that the content is valid JSON.
        new_view_definition = json.loads(result.content)
    except Exception as error:
        print(error)
        return commit_retry(state)
    
    # Validate the view definition
    try:
        body = {
            "viewDefinition": new_view_definition
        }
        sof_js_url = f"{SQL_ON_FHIR_API_URL}/validate"
        response = requests.post(sof_js_url, json=body)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error during view definition validation: {e}")
        return commit_retry(state)

    return add_view_definition(state, result.content)
