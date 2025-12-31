import logging
from core.config import DATABASE_URL
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

logger = logging.getLogger(__name__)

async def get_checkpointer():
    if not DATABASE_URL:
        logger.warning("Checkpointing disabled (DATABASE_URL missing)")
        return None

    return AsyncPostgresSaver.from_conn_string(DATABASE_URL)
