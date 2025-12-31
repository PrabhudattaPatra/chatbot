from langchain.messages import ToolMessage, AIMessage
from graph.workflow import build_graph
from langchain_groq import ChatGroq
from core.config import ANSWER_MODEL_NAME

llm = ChatGroq(model=ANSWER_MODEL_NAME, temperature=0)

def rag_target(inputs: dict) -> dict:
    """
    Target function for LangSmith evaluation.
    """
    question = inputs["question"]

    graph = build_graph(llm)
    final_state = graph.invoke({
        "messages": [{"role": "user", "content": question}]
    })

    final_answer = None
    final_documents = None

    for msg in final_state["messages"]:
        if isinstance(msg, ToolMessage):
            final_documents = msg.content
        if isinstance(msg, AIMessage):
            final_answer = msg.content

    return {
        "answer": final_answer,
        "documents": final_documents
    }
