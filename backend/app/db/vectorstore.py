from app.core.config import settings
from pinecone import Pinecone


def get_vector_index():
    """
    Dependency-injectable Pinecone index.
    Usage: Depends(get_vector_index) in your routers/services.
    """

    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    index_name = "developer-quickstart-py"

    if index_name not in pc.list_indexes().names():
        from pinecone import ServerlessSpec
        pc.create_index(
            name=index_name,
            dimension=1536, 
            metric="cosine",  
            spec=ServerlessSpec(cloud="azure", region=settings.PINECONE_ENV)  
        )

    index = pc.Index(index_name)
    
    yield index