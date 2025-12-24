import hashlib
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the directory where this file (store.py) is located
_STORE_DIR = Path(__file__).parent.resolve()
client = chromadb.PersistentClient(path=str(_STORE_DIR))

voyageai_ef = embedding_functions.VoyageAIEmbeddingFunction(
    api_key=os.getenv("VOYAGE_API_KEY"),  
    model_name="voyage-3-large"
)

class VectorStore:
    """Wrapper around ChromaDB collection."""
    
    def __init__(
        self,
        client: chromadb.ClientAPI,
        embedding_function = voyageai_ef,
        collection_name: str = "collection",
    ):
        self.client = client
        self.embedding_function = embedding_function
        self.collection_name = collection_name
        
        # Get or create collection with HNSW config
        try:
            self.collection = client.create_collection(
                name=collection_name,
                embedding_function=embedding_function,
                configuration={
                    "hnsw": {
                        "space": "cosine",
                        "ef_construction": 100
                    }
                }
            )
            logger.info(f"Collection {collection_name} created")
        except:
            self.collection = client.get_collection(
                name=collection_name,
                embedding_function=embedding_function
            )
            logger.info(f"Collection {collection_name} already exists")
    
    def generate_id(self, text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()[:16]
    
    def add(
        self,
        documents: list[str],
        metadatas: list[dict],
        ids: list[str] | None = None,
    ) -> list[str]:
        """Add documents to collection."""
        if ids is None:
            ids = [self.generate_id(doc) for doc in documents]
        
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
        )
        logger.info(f"Added {len(documents)} documents to collection {self.collection_name}")
        return ids
    
    def query(
        self,
        query_texts: list[str],
        n_results: int = 10,
        include: list[str] | None = None,
    ):
        """Query collection."""
        include = include or ["documents", "metadatas", "distances"]
        return self.collection.query(
            query_texts=query_texts,
            n_results=n_results,
            include=include,
        )
    
    def query_formatted(
        self,
        query_texts: list[str],
        n_results: int = 10,
    ):
        """Query and format results."""
        # TODO
        return self.query(query_texts, n_results)
    
    def count(self) -> int:
        """Return number of items in collection."""
        return self.collection.count()

    def delete(self) -> None:
        """Delete collection."""
        self.client.delete_collection(name=self.collection_name)
        logger.info(f"Collection {self.collection_name} deleted")
