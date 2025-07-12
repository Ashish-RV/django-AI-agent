from documents.models import Document
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from django.db.models import Q

@tool
def search_query_documents(query: str,limit:int=5, config:RunnableConfig =None):
    """
    Search the most recent LIMIT documents for the current user
    arguments:
    query: string or lookup search across title or content of document
    limit: number of results
    """
    #print(config)
    limit = 5
    configurable = config.get("metadata") or config.get("configurable")
    user_id = configurable.get("user_id")
    lookups = {
        "owner_id": user_id,
        "active": True,
        "title_icontains": query
    }
    qs = Document.objects.filter(**lookups).filter(
        Q(title__icontains=query) |
        Q(content__icontains=query)
    ).order_by("-created_at")
    response_data = []
    for obj in qs[:limit]:
        response_data.append({
            "id": obj.id,
            "title": obj.title
        })
    return response_data

@tool
def list_documents(config:RunnableConfig):
    """
    List the most recent LIMIT documents for the current user with maximum of 25.

    agruments
    limit: number of results
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

@tool
def update_document(document_id:int, title:str =None, content:str = None, config:RunnableConfig=None):
    """
    Update a document for a user by the document id and related arguments.

    Arguments are:
    document_id: id of document (required)
    title: string max characters of 120 (optional)
    content: long form text in many paragraphs or pages (optional)
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception("Invalid request for user.")
    #has_perms = async_to_sync(permit.check)(f"{user_id}", "update", "document")
    if not has_perms:
        raise Exception("You do not have permission to update individual documents.")
    try:
        obj = Document.objects.get(id=document_id, owner_id=user_id, active=True)
    except Document.DoesNotExist:
        raise Exception("Document not found, try again")
    except:
        raise Exception("Invalid request for a document detail, try again")
    
    if title is not None:
        obj.title = title
    if content is not None:
        obj.content = content
    if title or content:
        obj.save()
    # obj = Document.objects.create(title=title, content=content, owner_id=user_id, active=True)
    response_data =  {
        "id": obj.id,
        "title": obj.title,
        "content": obj.content,
        "created_at": obj.created_at
    }
    return response_data


@tool
def delete_document(document_id:int, config:RunnableConfig):
    """
    Delete  the  documents
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
    obj.delete()
    response_data = {"message":"success"}
    return response_data

document_tools = [
    create_document,
    list_documents,
    get_document,
    delete_document
]