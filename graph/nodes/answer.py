from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from graph.prompts import GENERATE_SYSTEM_PROMPT
from graph.common import get_latest_user_question

def generate_answer(state, llm):
    """Generate an answer."""
    question = get_latest_user_question(state["messages"])
    context = state["messages"][-1].content
    context_list = [m.content for m in state["messages"] if isinstance(m, ToolMessage)]
    context = "\n\n".join(context_list)
    retry_count = state.get("answer_retry_count", 0)

    messages = [
        SystemMessage(content=GENERATE_SYSTEM_PROMPT),
        HumanMessage(content=f"""
Use the following pieces of retrieved context to answer the question. 
If tools answer is not related to the user question, just say that you don't know. 
Question: {question}
Context: {context}
""")
    ]

    response = llm.invoke(messages)
    return {
        "messages": [response],
        "answer_retry_count": retry_count + 1
    }


