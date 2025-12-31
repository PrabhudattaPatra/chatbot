from ingestion.common.scraper_base import scrape_table
from ingestion.common.document_builder import build_and_ingest_documents
from ingestion.notice_board.config import NOTICE_URL, INDEX_NAME
from ingestion.notice_board.summarizer import get_notice_summarizer

def run_notice_ingestion():
    records = scrape_table(NOTICE_URL)
    model = get_notice_summarizer()

    build_and_ingest_documents(
        records=records,
        summarizer_model=model,
        index_name=INDEX_NAME,
    )
