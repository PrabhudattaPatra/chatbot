from langchain.messages import HumanMessage, ToolMessage
from graph.prompts import REWRITE_PROMPT
from graph.common import get_latest_user_question
def rewrite_question(state, llm):
    """Rewrite the original user question."""
    messages = state["messages"]
    # Safety: do not rewrite if tool already returned content
    if any(isinstance(m, ToolMessage) and m.content.strip() for m in messages):
        return {"rewrite_count": state.get("rewrite_count", 0)}
    question = get_latest_user_question(messages)

    current_count = state.get("rewrite_count", 0)
    prompt = REWRITE_PROMPT.format(question=question)
    response = llm.invoke([{"role": "user", "content": prompt}])
    return {
        "messages": [HumanMessage(content=response.content)],
        "rewrite_count": current_count + 1
    }

