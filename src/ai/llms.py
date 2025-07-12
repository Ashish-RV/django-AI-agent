from langchain_openai import ChatOpenAI, OpenAI
#from langchain.chat_models import ChatOpenAI
from django.conf import settings
from langchain_core.language_models.llms import LLM


def get_openai_api_key():
    return settings.OPEN_API_KEY

def get_openai_model(model="llama-3.2-1b-instruct"):
    # if model is None:
    #     model = "gpt-4o-mini"
    # elif model=="openai-community_-_gpt2-xl":
    #     return OpenAI(
    #             openai_api_key="not-needed",
    #             openai_api_base="http://localhost:1234/v1",
    #             model_name="openai-community_-_gpt2-xl",
    #         )
    return ChatOpenAI(
            model=model,
            base_url="http://127.0.0.1:1234/v1",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key= get_openai_api_key(),
    )
    