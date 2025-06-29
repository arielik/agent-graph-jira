"""ChromaDB client for vector storage and retrieval."""

import asyncio
from typing import List, Dict, Any, Optional

try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    chromadb = None

from loguru import logger

from src.utils.config import get_app_settings


class ChromaClient:
    """ChromaDB client for vector storage operations."""
    
    def __init__(self, collection_name: str = "jira_stories"):
        """Initialize ChromaDB client.
        
        Args:
            collection_name: Name of the ChromaDB collection
        """
        if chromadb is None:
            raise ImportError("ChromaDB not installed. Install with: pip install chromadb")
        
        self.settings = get_app_settings()
        self.collection_name = collection_name
        self._client: Optional[chromadb.Client] = None
        self._collection: Optional[chromadb.Collection] = None
    
    @property
    def client(self) -> chromadb.Client:
        """Get or create ChromaDB client.
        
        Returns:
            ChromaDB client instance
        """
        if self._client is None:
            self._client = chromadb.PersistentClient(
                path=self.settings.chroma_persist_directory,
                settings=Settings(anonymized_telemetry=False)
            )
        return self._client
    
    @property
    def collection(self) -> chromadb.Collection:
        """Get or create ChromaDB collection.
        
        Returns:
            ChromaDB collection instance
        """
        if self._collection is None:
            try:
                self._collection = self.client.get_collection(name=self.collection_name)
            except Exception:
                # Collection doesn't exist, create it
                self._collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "JIRA stories and templates for RAG"}
                )
                logger.info(f"Created ChromaDB collection: {self.collection_name}")
        
        return self._collection
    
    async def add_documents(
        self, 
        documents: List[str], 
        metadatas: List[Dict[str, Any]],
        ids: List[str]
    ) -> None:
        """Add documents to the vector database.
        
        Args:
            documents: List of document texts
            metadatas: List of metadata dictionaries
            ids: List of document IDs
        """
        try:
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
            )
            
            logger.info(f"Added {len(documents)} documents to ChromaDB")
            
        except Exception as e:
            logger.error(f"Failed to add documents to ChromaDB: {e}")
            raise
    
    async def search_similar(
        self, 
        query: str, 
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents.
        
        Args:
            query: Search query
            n_results: Number of results to return
            filter_metadata: Optional metadata filter
            
        Returns:
            List of similar documents with metadata
        """
        try:
            results = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.collection.query(
                    query_texts=[query],
                    n_results=n_results,
                    where=filter_metadata
                )
            )
            
            # Format results
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    formatted_results.append({
                        'document': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else 0.0,
                        'id': results['ids'][0][i] if results['ids'] else None
                    })
            
            logger.info(f"Found {len(formatted_results)} similar documents")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to search ChromaDB: {e}")
            raise
    
    async def delete_collection(self) -> None:
        """Delete the collection."""
        try:
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.delete_collection(name=self.collection_name)
            )
            
            self._collection = None
            logger.info(f"Deleted ChromaDB collection: {self.collection_name}")
            
        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
            raise
    
    async def get_collection_info(self) -> Dict[str, Any]:
        """Get collection information.
        
        Returns:
            Dictionary with collection information
        """
        try:
            count = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.collection.count()
            )
            
            return {
                'name': self.collection_name,
                'count': count,
                'metadata': self.collection.metadata
            }
            
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            raise
