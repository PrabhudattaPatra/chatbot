import logging
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from core.config import EMBEDDING_MODEL_NAME

logger = logging.getLogger(__name__)

_embedding_instance = None  

def get_embeddings() -> HuggingFaceEmbeddings:
    global _embedding_instance

    if _embedding_instance is None:
        logger.info(f"Loading embeddings: {EMBEDDING_MODEL_NAME}")
        _embedding_instance = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={"trust_remote_code": True}
        )

    return _embedding_instance
