import logging
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from core.config import (
    PINECONE_API_KEY,
    EMBEDDING_DIMENSION
)

logger = logging.getLogger(__name__)

_pinecone_client: Pinecone | None = None

def get_pinecone_client() -> Pinecone:
    global _pinecone_client

    if _pinecone_client is None:
        logger.info("Initializing Pinecone client")
        _pinecone_client = Pinecone(api_key=PINECONE_API_KEY)

    return _pinecone_client


def get_vector_store(
    index_name: str,
    embeddings,
    metric: str = "cosine"
) -> PineconeVectorStore:
    pc = get_pinecone_client()

    if not pc.has_index(index_name):
        logger.info(f"Creating Pinecone index: {index_name}")
        pc.create_index(
            name=index_name,
            dimension=EMBEDDING_DIMENSION,
            metric=metric,
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            ),
        )

    index = pc.Index(index_name)
    logger.info(f"Connected to Pinecone index: {index_name}")

    return PineconeVectorStore(
        index=index,
        embedding=embeddings
    )
