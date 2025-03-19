# import getpass
# import os
# from langchain_community.document_loaders import UnstructuredHTMLLoader
# from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic
# from langchain_core.messages import HumanMessage, SystemMessage

# fhir_patient_docs = "./assets/html/Patient - FHIR v5.0.0.html"
# fhir_view_definition_docs = "./assets/html/View Definition - SQL on FHIR v2.0.0-pre.html"

# # Check if file exists
# try:
#     with open(fhir_patient_docs) as f:
#         pass
# except FileNotFoundError:
#     print(f"File {fhir_patient_docs} not found")
#     exit(1)
    
# # Check for openai key
# # if "OPENAI_API_KEY" not in os.environ:
# #     os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

# # Check for anthropic key
# if "ANTHROPIC_API_KEY" not in os.environ:
#     os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter your Anthropic API key: ")

# # Load the patient HTML
# patient_loader = UnstructuredHTMLLoader(fhir_patient_docs)
# patient_html = patient_loader.load()

# # Load the view definition HTML
# view_definition_loader = UnstructuredHTMLLoader(fhir_view_definition_docs)
# view_definition_html = view_definition_loader.load()

# # Convert the documents to a single string
# patient_content = ""
# for doc in patient_html:
#     patient_content += doc.page_content + "\n\n"
    
# view_definition_content = ""
# for doc in view_definition_html:
#     view_definition_content += doc.page_content + "\n\n"

# # System message
# sys_prompt = "You are a FHIR expert, you have all the required about the patient resource here: " + patient_content + "." + "You also have the view definition here: " + view_definition_content + ". You are going to be asked questions about creating views on the patient resource. You need to answer the questions based on the information you have."
# sys_msg = SystemMessage(sys_prompt)

# # Human message
# hum_msg = HumanMessage("Show the patient's name and address?")

# # llm = ChatOpenAI(model="o3-mini")
# llm = ChatAnthropic(model="claude-3-7-sonnet-20250219")

# result = llm.invoke([sys_msg, hum_msg])
# print(result.content)

from langgraph.graph import StateGraph, START, END
from state.state import PromptState
from nodes.get_user_question import get_user_question
from nodes.get_requested_resource import get_requested_resource
from nodes.get_view_definition import get_view_definition
from nodes.handle_view_definition import handle_view_definition

# Build graph
builder = StateGraph(PromptState)
builder.add_node("get_user_question", get_user_question)
builder.add_node("get_requested_resource", get_requested_resource)
builder.add_node("get_view_definition", get_view_definition)
builder.add_node("handle_view_definition", handle_view_definition)
builder.add_edge(START, "get_user_question")
builder.add_edge("get_user_question", "get_requested_resource")
builder.add_edge("get_requested_resource", "get_view_definition")
builder.add_edge("get_view_definition", "handle_view_definition")
builder.add_edge("handle_view_definition", END)
graph = builder.compile()

state = graph.invoke({"user_question": "What is John Smith's latest blood pressure?", "requested_resource": None, "view_definition": None, "should_retry": False, "retry_count": 0})
