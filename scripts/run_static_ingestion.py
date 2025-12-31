"""
Run static document ingestion.
Usage:
    python scripts/run_static_ingestion.py
"""

import logging
from core.logging import setup_logging

from ingestion.static_docs.loader import load_static_documents
from ingestion.static_docs.splitter import get_text_splitter
from ingestion.static_docs.pipeline import ingest_static_documents

STATIC_DOCS_PATH = "data/static_docs"  # change if needed

def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting static document ingestion")

    documents = load_static_documents(STATIC_DOCS_PATH)
    splitter = get_text_splitter()
    split_docs = splitter.split_documents(documents)

    ingest_static_documents(split_docs)

    logger.info("Static document ingestion completed successfully")


if __name__ == "__main__":
    main()
