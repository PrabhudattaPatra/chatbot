import logging
from core.embedding_model import get_embeddings
from core.pinecone_client import get_vector_store
from core.config import STATIC_INDEX_NAME

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    return text.encode("utf-8", "ignore").decode("utf-8", "ignore")


def ingest_static_documents(documents):
    embeddings = get_embeddings()
    vector_store = get_vector_store(STATIC_INDEX_NAME, embeddings)

    for doc in documents:
        doc.page_content = clean_text(doc.page_content)

    logger.info(f"Adding {len(documents)} static documents to Pinecone")
    vector_store.add_documents(documents)
