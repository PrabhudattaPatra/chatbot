# graph/checkpointing.py
import logging
from core.config import DATABASE_URL
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

logger = logging.getLogger(__name__)

_checkpointer = None

async def get_checkpointer():
    global _checkpointer

    if _checkpointer is not None:
        return _checkpointer

    if not DATABASE_URL:
        logger.warning("Checkpointing disabled (DATABASE_URL not set)")
        return None

    logger.info("Initializing AsyncPostgresSaver")

    _checkpointer = await AsyncPostgresSaver.from_conn_string(
        DATABASE_URL
    )

    return _checkpointer
