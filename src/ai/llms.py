from langchain_openai import ChatOpenAI
from django.conf import settings


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