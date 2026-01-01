import logging
import uuid
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langchain_core.messages import ToolMessage

from core.config import ANSWER_MODEL_NAME, DATABASE_URL
from graph.workflow import build_graph

# --- Global Graph State ---
# This holds the compiled graph to be reused across all requests
app_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles setup and teardown of the global graph and database pool."""
    
    # 1. Correctly enter the AsyncPostgresSaver context manager
    async with AsyncPostgresSaver.from_conn_string(DATABASE_URL) as checkpointer:
        
        # 2. Setup the LLM
        llm = ChatGroq(
            model=ANSWER_MODEL_NAME, 
            temperature=0
        )
        
        # 3. Build and Compile the graph ONCE
        # The checkpointer is now the actual object, not a context manager
        app_state["graph"] = build_graph(llm, checkpointer=checkpointer)
        
        print("Application startup complete: Graph and Checkpointer initialized.")
        
        yield  # The app stays in this state while running
        
    # Connections are automatically closed when exiting the 'async with' block
    app_state.clear()

app = FastAPI(title="CGU RAG Agent API", lifespan=lifespan)

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None

class ChatResponse(BaseModel):
    thread_id: str
    response: str
    updates: List[Dict[str, Any]]
    used_retrievers: List[str] = []

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    thread_id = request.thread_id or str(uuid.uuid4())
    
    # Configuration including the thread_id for state retrieval
    CONFIG = {
        "configurable": {"thread_id": thread_id},
        "metadata": {"thread_id": thread_id},
        "run_name": "chat_turn",
    }
    
    inputs = {"messages": [{"role": "user", "content": request.message}]}
    final_response = ""
    node_updates = []
    triggered_retrievers = set()

    # Access the pre-compiled graph from global state
    graph = app_state.get("graph")
    if not graph:
        raise HTTPException(status_code=500, detail="Graph not initialized")

    try:
        # We only call .astream(), no building or compiling happens here
        async for chunk in graph.astream(inputs, CONFIG, stream_mode="updates"):
            for node, update in chunk.items():
                if "messages" in update:
                    for msg in update["messages"]:
                        # Capture tool usage (retrievers)
                        if isinstance(msg, ToolMessage):
                            triggered_retrievers.add(msg.name) 
                        
                        node_updates.append({
                            "node": node, 
                            "content": str(msg.content),
                            "type": msg.__class__.__name__
                        })

                    # Final answer capture [cite: 538, 615]
                    if node == "generate_answer":
                        final_response = update["messages"][-1].content

        if not final_response and node_updates:
            final_response = node_updates[-1]["content"]

        return ChatResponse(
            thread_id=thread_id,
            response=final_response,
            updates=node_updates,
            used_retrievers=list(triggered_retrievers)
        )

    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")