from qdrant_client import QdrantClient
from qdrant_client.http import models
from config.settings import settings
from typing import List, Dict, Any
import logging


logger = logging.getLogger(__name__)


class VectorService:
    def __init__(self):
        # Initialize Qdrant client
        if settings.qdrant_api_key:
            self.client = QdrantClient(
                url=settings.qdrant_host,
                api_key=settings.qdrant_api_key,
                prefer_grpc=False  # Using HTTP for simplicity
            )
        else:
            self.client = QdrantClient(url=settings.qdrant_host)
        
        # Collection name for document chunks
        self.collection_name = "document_chunks"
        
        # Initialize the collection if it doesn't exist
        self._init_collection()
    
    def _init_collection(self):
        """Initialize the Qdrant collection if it doesn't exist"""
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)
            
            if not collection_exists:
                # Create collection with vector configuration
                # Using 768 dimensions as a common size for sentence transformers
                # In a real application, this would need to match your embedding model's output size
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
                )
                
                logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                logger.info(f"Qdrant collection already exists: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error initializing Qdrant collection: {str(e)}")
            raise
    
    async def store_embedding(self, chunk_id: str, embedding: List[float], metadata: Dict[str, Any]):
        """Store a document chunk embedding in Qdrant"""
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=chunk_id,
                        vector=embedding,
                        payload=metadata
                    )
                ]
            )
            return True
        except Exception as e:
            logger.error(f"Error storing embedding: {str(e)}")
            return False
    
    async def search_similar(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar document chunks based on the query embedding"""
        try:
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                with_payload=True
            )
            
            results = []
            for hit in search_results:
                result = {
                    'id': hit.id,
                    'score': hit.score,
                    'payload': hit.payload
                }
                results.append(result)
            
            return results
        except Exception as e:
            logger.error(f"Error searching for similar embeddings: {str(e)}")
            return []
    
    async def delete_embedding(self, chunk_id: str):
        """Delete a specific chunk embedding from Qdrant"""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(points=[chunk_id])
            )
            return True
        except Exception as e:
            logger.error(f"Error deleting embedding: {str(e)}")
            return False
    
    async def delete_by_document_id(self, document_id: str):
        """Delete all chunks associated with a specific document"""
        try:
            # Create a filter to find all points with the given document_id
            filter_condition = models.Filter(
                must=[
                    models.FieldCondition(
                        key="document_id",
                        match=models.MatchValue(value=document_id)
                    )
                ]
            )
            
            # Delete all points matching the filter
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.FilterSelector(filter=filter_condition)
            )
            return True
        except Exception as e:
            logger.error(f"Error deleting embeddings by document ID: {str(e)}")
            return False