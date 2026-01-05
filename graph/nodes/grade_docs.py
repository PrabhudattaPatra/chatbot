import logging
from typing import Literal
from core.models import GradeDocuments
from graph.prompts import GRADE_PROMPT
from graph.common import get_latest_user_question 
logger = logging.getLogger(__name__)




def grade_documents(state, llm) -> Literal["generate_answer", "rewrite_question"]:
    question = get_latest_user_question(state["messages"])
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
