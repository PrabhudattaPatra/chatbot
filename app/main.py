import json
import uuid
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from langchain_groq import ChatGroq
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langchain_core.messages import AIMessageChunk

# Imports from your project structure
from core.config import ANSWER_MODEL_NAME, DATABASE_URL
from graph.workflow import build_graph

app_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes the graph and database connection once at startup."""
    async with AsyncPostgresSaver.from_conn_string(DATABASE_URL) as checkpointer:
        # Enable streaming at the LLM level for real-time tokens
        llm = ChatGroq(model=ANSWER_MODEL_NAME, temperature=0, streaming=True)
        # build_graph should return the compiled graph using the checkpointer
        app_state["graph"] = build_graph(llm, checkpointer=checkpointer)
        print("Backend Ready: Streaming Graph Initialized.")
        yield
    app_state.clear()

app = FastAPI(title="CGU RAG Streaming API", lifespan=lifespan)

# Essential CORS middleware for Frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    thread_id = request.thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    inputs = {"messages": [{"role": "user", "content": request.message}]}
    
    graph = app_state.get("graph")
    if not graph:
        raise HTTPException(status_code=500, detail="Graph not initialized")

    async def stream_generator():
        triggered_tools = set()
        
        # 'messages' stream_mode allows capturing token deltas in real-time
        async for msg, metadata in graph.astream(inputs, config, stream_mode="messages"):
            # 1. Detect and stream Tool Usage (for source badges)
            if isinstance(msg, AIMessageChunk) and msg.tool_call_chunks:
                for chunk in msg.tool_call_chunks:
                    if chunk.get("name"):
                        tool_name = chunk["name"]
                        if tool_name not in triggered_tools:
                            triggered_tools.add(tool_name)
                            yield f"data: {json.dumps({'type': 'tool', 'name': tool_name})}\n\n"

            # 2. Stream AI Response Content (text tokens)
            if isinstance(msg, AIMessageChunk) and msg.content:
                yield f"data: {json.dumps({'type': 'content', 'delta': msg.content})}\n\n"

        # 3. Final event to provide the current thread_id to the frontend
        yield f"data: {json.dumps({'type': 'end', 'thread_id': thread_id})}\n\n"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# uvicorn app.main:app --reload
