import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from graph.workflow import build_graph
from graph.checkpointing import get_checkpointer

from langchain_groq import ChatGroq
from core.config import ANSWER_MODEL_NAME

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Query"])

# ===============================
# Request / Response Schemas
# ===============================
class ChatRequest(BaseModel):
    question: str = Field(..., min_length=3)
    thread_id: Optional[str] = Field(
        default="default",
        description="Conversation thread id"
    )


class ChatResponse(BaseModel):
    answer: str


# ===============================
# Initialize LLM once
# ===============================
llm = ChatGroq(
    model=ANSWER_MODEL_NAME,
    temperature=0,
)


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    try:
        checkpointer = await get_checkpointer()
        graph = build_graph(llm, checkpointer=checkpointer)

        inputs = {
            "messages": [
                {"role": "user", "content": payload.question}
            ]
        }

        config = {
            "configurable": {
                "thread_id": payload.thread_id
            }
        }

        final_answer = None

        async for chunk in graph.astream(
            inputs,
            config,
            stream_mode="updates"
        ):
            for _, update in chunk.items():
                if "messages" in update:
                    final_answer = update["messages"][-1].content

        if not final_answer:
            raise ValueError("No response generated")

        return ChatResponse(answer=final_answer)

    except Exception as exc:
        logger.exception("Chat endpoint failed")
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
