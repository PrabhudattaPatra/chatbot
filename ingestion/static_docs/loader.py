import logging
from langchain_community.document_loaders import PyPDFDirectoryLoader

logger = logging.getLogger(__name__)

def load_static_documents(path: str):
    logger.info(f"Loading static PDFs from {path}")
    loader = PyPDFDirectoryLoader(path)
    return loader.load()
