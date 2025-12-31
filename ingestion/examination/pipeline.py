from ingestion.common.scraper_base import scrape_table
from ingestion.common.document_builder import build_and_ingest_documents
from ingestion.examination.config import EXAM_URL, INDEX_NAME
from ingestion.examination.summarizer import get_exam_summarizer

def run_exam_ingestion():
    records = scrape_table(EXAM_URL)
    model = get_exam_summarizer()

    build_and_ingest_documents(
        records=records,
        summarizer_model=model,
        index_name=INDEX_NAME,
    )
