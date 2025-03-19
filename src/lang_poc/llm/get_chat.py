from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from typing import Literal

ANTHROPIC_MODEL = "claude-3-7-sonnet-20250219"
OPENAI_MODEL = "o3-mini"

def get_chat_anthropic():
    return ChatAnthropic(model=ANTHROPIC_MODEL)

def get_chat_openai():
    return ChatOpenAI(model=OPENAI_MODEL)

def get_chat(model: Literal["anthropic", "openai"] = "anthropic"):
    if model == "anthropic":
        return get_chat_anthropic()
    return get_chat_openai()
