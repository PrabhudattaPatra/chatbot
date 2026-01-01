import logging
from typing import Literal
from langchain_core.messages import ToolMessage, HumanMessage
from core.models import GradeDocuments
from graph.prompts import GRADE_PROMPT

logger = logging.getLogger(__name__)



def _latest_user_question(messages):
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            return msg.content
    return ""

def grade_documents(state, llm) -> Literal["generate_answer", "rewrite_question"]:
    question = _latest_user_question(state["messages"])
    rewrite_count = state.get("rewrite_count", 0)

    context = state["messages"][-1].content
    prompt = GRADE_PROMPT.format(question=question, context=context)

    result = llm.with_structured_output(GradeDocuments).invoke(
        [{"role": "user", "content": prompt}]
    )

    logger.info(
        f"Document relevance: {result.binary_score} "
        f"(rewrite_count={rewrite_count})"
    )

    if rewrite_count >= 2:
        return "generate_answer"

    return (
        "generate_answer"
        if result.binary_score == "yes"
        else "rewrite_question"
    )
