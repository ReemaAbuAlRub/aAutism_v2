from typing import List, Optional, Dict, Any


class EmbeddingRepository:
    def __init__(self, index):
        self.index = index
    
    def upsert(self, id: str, vector: List[float], metadata: Dict) -> None:
        """
        Insert or update a vector in the index.
        """
        self.index.upsert(vectors=[(id, vector, metadata)])
    
    def upsert_batch(self, vectors: List[tuple]) -> None:
        """
        Insert or update multiple vectors in batch.
        vectors: List of tuples (id, vector, metadata)
        """
        self.index.upsert(vectors=vectors)
    
    def query(
            self,
            vector: List[float],
            top_k: int = 8,
            include_metadata: bool = True,
            metadata_filter: Optional[Dict[str, Any]] = None,
        ):
            # Why: use 'filter' (dict) and includeMetadata=True to get metadata back
            res = self.index.query(
                vector=vector,
                top_k=top_k,
                include_metadata=include_metadata,
                filter=metadata_filter or {},
            )
            return getattr(res, "matches", []) or []
    
    def query_by_id(self, id: str, top_k: int = 5, namespace: Optional[str] = None):
        """
        Query the index using an existing vector ID.
        """
        response = self.index.query(
            id=id,
            top_k=top_k,
            include_metadata=True,
            namespace=namespace
        )
        return response.matches
    
    def delete(self, ids: List[str], namespace: Optional[str] = None) -> None:
        """
        Delete vectors by their IDs.
        """
        self.index.delete(ids=ids, namespace=namespace)
    
    def delete_all(self, namespace: Optional[str] = None) -> None:
        """
        Delete all vectors in the index or namespace.
        """
        self.index.delete(delete_all=True, namespace=namespace)
    
    def fetch(self, ids: List[str], namespace: Optional[str] = None):
        """
        Fetch vectors by their IDs.
        """
        response = self.index.fetch(ids=ids, namespace=namespace)
        return response.vectors
    
    def get_stats(self, namespace: Optional[str] = None):
        """
        Get index statistics.
        """
        return self.index.describe_index_stats(namespace=namespace)