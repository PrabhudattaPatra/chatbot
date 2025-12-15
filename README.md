# RAG-based Chatbot with Self-Correction and Hallucination Detection

A sophisticated Retrieval-Augmented Generation (RAG) chatbot system built with LangGraph that features document retrieval, answer generation, quality grading, and hallucination detection for C.V. Raman Global University (CGU) queries.

## 🌟 Features

- **Intelligent Document Retrieval**: Uses ChromaDB vector store with OpenAI embeddings for semantic search
- **Multi-Source Information**: Combines local document retrieval with web search using Tavily
- **Self-Correcting RAG**: Automatically grades document relevance and rewrites queries if needed
- **Hallucination Detection**: Validates generated answers to ensure factual accuracy
- **Iterative Refinement**: Loops back to regenerate answers or rewrite questions based on quality checks
- **Loop Limiting**: Prevents infinite loops with configurable maximum retry attempts

## 🏗️ Architecture

The system uses a state graph with the following nodes:

1. **generate_query_or_respond**: Initial LLM call that decides whether to retrieve documents or respond directly
2. **retrieve**: Fetches relevant documents using retriever tool or web search
3. **grade_documents**: Evaluates document relevance to the user's question
4. **rewrite_question**: Reformulates the question if documents aren't relevant
5. **generate_answer**: Creates an answer based on retrieved context
6. **check_hallucination**: Validates the answer for factual accuracy

## 📋 Prerequisites
```bash
uv add -r requirements.txt
```

## ⚙️ Environment Setup

Create a `.env` file with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## 📁 Project Structure
```
.
├── data/                          # PDF documents directory
├── my_chroma_db/                  # ChromaDB vector store
├── rag_copy.ipynb                 # Main notebook
├── .env                           # Environment variables
└── README.md                      # This file
```
## 🔄 Graph Workflow
The RAG system follows this workflow:

![RAG Workflow Graph](/image/workflow_graph.jpg)