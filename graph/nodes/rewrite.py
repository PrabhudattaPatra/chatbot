from langchain.messages import HumanMessage, ToolMessage
from graph.prompts import REWRITE_PROMPT

def rewrite_question(state, llm):
    messages = state["messages"]

    # 🔒 Do NOT rewrite if tools already returned content
    if any(isinstance(m, ToolMessage) and m.content.strip() for m in messages):
        return {"rewrite_count": state.get("rewrite_count", 0)}

    question = next(
        m.content for m in reversed(messages) if isinstance(m, HumanMessage)
    )

    prompt = REWRITE_PROMPT.format(question=question)
    response = llm.invoke([{"role": "user", "content": prompt}])

    return {
        "messages": [HumanMessage(content=response.content)],
        "rewrite_count": state.get("rewrite_count", 0) + 1,
    }
