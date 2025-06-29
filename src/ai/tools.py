from documents.models import Document
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool


@tool
def list_documents(config:RunnableConfig):
    """
    List the most recent 5 documents for the current user
    """
    #print(config)
    limit = 5
    configurable = config.get("metadata") or config.get("configurable")
    user_id = configurable.get("user_id")
    qs = Document.objects.filter(owner_id = user_id,active=True).order_by("-created_at")
    response_data = []
    for obj in qs[:limit]:
        response_data.append({
            "id": obj.id,
            "title": obj.title
        })
    return response_data


@tool
def get_document(document_id:int, config:RunnableConfig):
    """
    get the specfic documents
    """
    configurable = config.get("metadata") or config.get("configurable")
    user_id = configurable.get("user_id")
    if user_id is None:
        raise Exception("Invalid requests for user")
    try:
        obj = Document.objects.get(id = document_id,owner_id= user_id ,active=True)
    except Document.DoesNotExist:
        raise Exception("Document not found, try again")
    except:
        raise Exception("Invalid Request for Document, try again")
    response_data = []
    response_data.append({
            "id": obj.id,
            "title": obj.title,
            "content": obj.content,
            "created_at" : obj.created_at
        })
    return response_data

def create_document(title:str, content:str, config:RunnableConfig):
    """
    Create a new document based on the argument
    title: string amx charaters of 120
    content: long form text in many paragraphs or pages
    """
    configurable = config.get("metadata") or config.get("configurable")
    user_id = configurable.get("user_id")
    if user_id is None:
        raise Exception("Invalid requests for user")
    try:
        obj = Document.objects.create(title=title, content=content,owner_id= user_id ,active=True)
    except Document.DoesNotExist:
        raise Exception("Document not found, try again")
    except:
        raise Exception("Invalid Request for Document, try again")
    response_data = []
    response_data.append({
            "id": obj.id,
            "title": obj.title,
            "content": obj.content,
            "created_at" : obj.created_at
        })
    return response_data


document_tools = [
    create_document,
    list_documents,
    get_document
]