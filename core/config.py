import os
import logging
from dotenv import load_dotenv
from pathlib import Path

logger = logging.getLogger(__name__)

ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(ENV_PATH)

# ===============================
# Environment
# ===============================
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# ===============================
# API Keys
# ===============================
PINECONE_API_KEY: str | None = os.getenv("PINECONE_API_KEY")
DATABASE_URL: str | None = os.getenv("DATABASE_URL")

if not PINECONE_API_KEY:
    raise RuntimeError("❌ PINECONE_API_KEY is not set")

if ENVIRONMENT == "production" and not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL must be set in production")

if ENVIRONMENT != "production" and not DATABASE_URL:
    logger.warning(
        "⚠️ DATABASE_URL not found. "
        "Postgres checkpointing is disabled."
    )

# ===============================
# Pinecone Index Names
# ===============================
STATIC_INDEX_NAME = "cgu-test-index"
EXAM_INDEX_NAME = "cgu-examination-index"
NOTICE_INDEX_NAME = "cgu-notice-index"

# ===============================
# Embedding Configuration
# ===============================
EMBEDDING_MODEL_NAME = "nomic-ai/nomic-embed-text-v1.5"
EMBEDDING_DIMENSION = 768

# ===============================
# LLM Configuration
# ===============================
ANSWER_MODEL_NAME = "llama-3.3-70b-versatile"
VISION_MODEL_NAME = "gemini-2.5-flash-lite"

# ===============================
# General Settings
# ===============================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
