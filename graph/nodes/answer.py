from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from graph.prompts import GENERATE_SYSTEM_PROMPT

def generate_answer(state, llm):
    question = next(
        m.content for m in reversed(state["messages"])
        if isinstance(m, HumanMessage)
    )

    context = "\n\n".join(
        m.content for m in state["messages"]
        if isinstance(m, ToolMessage)
    )

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
        "answer_retry_count": state.get("answer_retry_count", 0) + 1,
    }
