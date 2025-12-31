import logging
from core.embedding_model import get_embeddings
from core.pinecone_client import get_vector_store
from core.config import (
    STATIC_INDEX_NAME,
    EXAM_INDEX_NAME,
    NOTICE_INDEX_NAME,
)

logger = logging.getLogger(__name__)

def build_retriever(
    index_name: str,
    k: int = 4,
    fetch_k: int = 20,
    lambda_mult: float = 0.6,
):
    embeddings = get_embeddings()
    vector_store = get_vector_store(index_name, embeddings)

    logger.info(f"Building retriever for index: {index_name}")

    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": k,
            "fetch_k": fetch_k,
            "lambda_mult": lambda_mult,
        },
    )


def get_static_retriever():
    return build_retriever(
        STATIC_INDEX_NAME,
        lambda_mult=0.6,
    )


def get_exam_retriever():
    return build_retriever(
        EXAM_INDEX_NAME,
        lambda_mult=0.5,
    )


def get_notice_retriever():
    return build_retriever(
        NOTICE_INDEX_NAME,
        lambda_mult=0.5,
    )
