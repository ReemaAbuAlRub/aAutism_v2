from app.core.config import settings
from pinecone import Pinecone
import pinecone


# def get_vector_index():
#     pc = Pinecone(api_key=settings.PINECONE_API_KEY)
#     index_name = "developer"

#     if index_name not in pc.list_indexes().names():
#         from pinecone import ServerlessSpec
#         pc.create_index(
#             name=index_name,
#             dimension=1536, 
#             metric="cosine",  
#             spec=ServerlessSpec(cloud="azure", region=settings.PINECONE_ENV)  
#         )

#     index = pc.Index(index_name)
    
#     return index

from pinecone import Pinecone, ServerlessSpec
from app.core.config import settings

def get_vector_index():
    """
    FastAPI dependency to get a ready-to-use Pinecone index.
    """
    # 1) Instantiate the client (no more pinecone.init)
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    
    index_name = "dev876786876876798-v2"



    existing = pc.list_indexes().names()
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
    
    return pc.Index(index_name)