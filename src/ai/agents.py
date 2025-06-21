from langgraph.prebuilt import create_react_agent
from llms import get_openai_model
from tools import (document_tools)

def get_agent():
    model = get_openai_model()
    agent = create_react_agent(
        model=model,
        tools=document_tools,
        prompt="You are a helpful assistant"
    )
    return agent