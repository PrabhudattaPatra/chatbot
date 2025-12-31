import logging
from uuid import uuid4
from langchain_core.documents import Document

from ingestion.common.ocr_utils import (
    pdf_url_to_images,
    pil_image_to_base64,
)
from ingestion.common.summarization import summarize_image_page
from core.embeddings import get_embeddings
from core.pinecone_client import get_vector_store

logger = logging.getLogger(__name__)

def build_and_ingest_documents(
    records: list[dict],
    summarizer_model,
    index_name: str,
):
    """
    Generic pipeline:
    records → PDF → images → multimodal summary → documents → Pinecone
    """

    if not records:
        logger.warning("No records provided for ingestion")
        return

    documents = []

    for record in records:
        logger.info(f"Processing PDF: {record['title']}")

        try:
            images = pdf_url_to_images(record["pdf_url"])
        except Exception:
            logger.warning(f"Skipping PDF: {record['pdf_url']}")
            continue

        page_summaries = []

        for idx, image in enumerate(images):
            image_b64 = pil_image_to_base64(image)
            summary = summarize_image_page(image_b64, summarizer_model)
            page_summaries.append(
                f"--- Page {idx + 1} ---\n{summary}"
            )

        documents.append(
            Document(
                page_content="\n\n".join(page_summaries),
                metadata={
                    "source": record["title"],
                    "date": record["publish_date"],
                    "pdf_url": record["pdf_url"],
                },
                id=record["id"],
            )
        )

    if not documents:
        logger.warning("No documents generated after processing")
        return

    embeddings = get_embeddings()
    vector_store = get_vector_store(index_name, embeddings)

    ids = [str(uuid4()) for _ in documents]
    vector_store.add_documents(documents, ids=ids)

    logger.info(
        f"Ingested {len(documents)} documents into index {index_name}"
    )
