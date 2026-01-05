# CGU Agentic RAG Bot

An advanced Multimodal Retrieval-Augmented Generation (RAG) system built with LangGraph, LangChain, FastAPI and Pinecone. It features a self-correcting loop that grades retrieved documents, rewrites queries for better accuracy, and performs hallucination checks before answering.

## Project Structure

The implementation is organized into modular components for scalability and maintainability:

**vector_store.py**  
Manages connections to Pinecone indices (`cgu-test-index`, `cgu-examination-index`, `cgu-notice-index`) and initializes HuggingFaceEmbeddings using the `nomic-embed-text-v1.5` model.

**tools.py**  
Defines specialized LangChain tools:

- `retrieve_blog_posts`: Fetches general university info (fees, admissions, scholarships).
- `retrieve_examination_cell_doc`: Fetches exam schedules and circulars.
- `retrieve_notice_board_doc`: Fetches academic calendar updates and official announcements.

**Note:** Documents are processed using a multimodal ingestion pipeline:  
Scan PDF → Images → OCR + LLM-based summarization → Stored in a dedicated examination vector store for fast retrieval.

- `websearch_tool`: Integrated via TavilySearch to monitor real-time updates from official social channels.

**agent.py**  
Contains the LangGraph state machine logic, including nodes for retrieval, grading, answering, and query rewriting.

**evaluation.py**  
Implements LangSmith evaluation suites for Correctness, Groundedness, Relevance, and Retrieval Relevance.

## Key Features

**Agentic Decision Making**  
The `generate_query_or_respond` node dynamically decides whether to use a tool or respond directly based on the user's intent.

**Multi-Index MMR Search**  
Uses Maximum Marginal Relevance (MMR) for diverse document retrieval across three distinct specialized indices.

**Self-Correction Loop**
- **Document Grading:** Evaluates retrieved documents on a binary `yes` / `no` scale for relevance.
- **Query Rewriting:** Automatically reformulates the question if initial retrieval is deemed irrelevant.
- **Hallucination Detection:** Compares the generated answer against the source context; if it fails twice, it returns the best available answer.

**State Persistence**  
Implements `AsyncPostgresSaver` for persistent thread management, allowing for multi-turn conversations.

## LangGraph Workflow

![RAG Workflow Graph](D:\abhi_project\image.png)

## Technical Stack

- **LLM:** `llama-3.3-70b-versatile` (via Groq) for primary reasoning and `gpt-4o` for evaluation.
- **Embeddings:** `nomic-ai/nomic-embed-text-v1.5`
- **Vector DB:** Pinecone (Serverless on AWS)
- **Frameworks:** LangChain, LangGraph, LangSmith

## Evaluation Metrics

The system is continuously evaluated using a dedicated dataset (CGU Q&A) and the following graders:

| Metric               | Description                                                     |
|----------------------|-----------------------------------------------------------------|
| Correctness          | Factual accuracy compared to Ground Truth                       |
| Groundedness         | Ensures the answer is derived strictly from provided FACTS      |
| Relevance            | Measures how well the answer addresses the user's QUESTION      |
| Retrieval Relevance  | Grades the quality of documents fetched by the retrievers       |
