from langgraph.prebuilt import create_react_agent
<<<<<<< HEAD
from ai.llms import get_openai_model
from ai.tools import (document_tools)

def get_document_agent():
=======
from llms import get_openai_model
from tools import (document_tools)

def get_agent():
>>>>>>> 43d4f3875b3c6d4d1e1f8e62f4615ea1bc370af2
    model = get_openai_model()
    agent = create_react_agent(
        model=model,
        tools=document_tools,
        prompt="You are a helpful assistant"
    )
    return agent