from langchain_openai import ChatOpenAI
from django.conf import settings

<<<<<<< HEAD
## hello
=======

>>>>>>> 43d4f3875b3c6d4d1e1f8e62f4615ea1bc370af2
def get_openai_api_key():
    return settings.OPEN_API_KEY

def get_openai_model(model="gpt-4o-mini"):
    return ChatOpenAI(
            model=model,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key= get_openai_api_key(),
    )