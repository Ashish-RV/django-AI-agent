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
    try:
        obj = Document.objects.get(id = document_id,owner_id= user_id ,active=True)
    except Document.DoesNotExist:
        raise Exception("Document not found, try again")
    except:
        raise Exception("Invalid Request for Document, try again")
    response_data = []
    response_data.append({
            "id": obj.id,
            "title": obj.title
        })
    return response_data


document_tools = [
    list_documents,
    get_document
]