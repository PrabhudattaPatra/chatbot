"""
Run examination document ingestion.
Usage:
    python scripts/run_examination_ingestion.py
"""

import logging
from core.logging import setup_logging

from ingestion.examination.pipeline import run_exam_ingestion

def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting examination ingestion")

    run_exam_ingestion()

    logger.info("Examination ingestion completed successfully")


if __name__ == "__main__":
    main()
