import logging
from fastapi import FastAPI

from core.logging import setup_logging
from app.routers.health import router as health_router
from app.routers.query import router as query_router

# ===============================
# Setup logging FIRST
# ===============================
setup_logging()
logger = logging.getLogger(__name__)

# ===============================
# Create FastAPI app
# ===============================
app = FastAPI(
    title="CGU RAG Agent",
    description="AI assistant for C.V. Raman Global University",
    version="1.0.0",
)

# ===============================
# Register routers
# ===============================
app.include_router(health_router)
app.include_router(query_router)

logger.info("CGU RAG Agent FastAPI app initialized")
