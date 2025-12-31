import logging
from typing import Literal
from pydantic import BaseModel, Field
from langchain.messages import HumanMessage
from langgraph.graph import END

from graph.prompts import HALLUCINATION_PROMPT

logger = logging.getLogger(__name__)

class HallucinationCheck(BaseModel):
    hallucination: Literal["yes", "no"] = Field(...)

def check_hallucination(state, llm):
    question = next(
        m.content for m in reversed(state["messages"])
        if isinstance(m, HumanMessage)
    )
    answer = state["messages"][-1].content
    retry_count = state.get("answer_retry_count", 0)

    prompt = HALLUCINATION_PROMPT.format(
        question=question,
        answer=answer,
    )

    result = llm.with_structured_output(HallucinationCheck).invoke(
        [{"role": "user", "content": prompt}]
    )

    logger.info(
        f"Hallucination={result.hallucination} "
        f"(retry_count={retry_count})"
    )

    if retry_count >= 2:
        return END

    return "generate_answer" if result.hallucination == "yes" else END
