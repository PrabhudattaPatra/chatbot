"""
Run notice board document ingestion.
Usage:
    python scripts/run_notice_ingestion.py
"""

import logging
from core.logging import setup_logging

from ingestion.notice_board.pipeline import run_notice_ingestion

def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting notice board ingestion")

    run_notice_ingestion()

    logger.info("Notice board ingestion completed successfully")


if __name__ == "__main__":
    main()
