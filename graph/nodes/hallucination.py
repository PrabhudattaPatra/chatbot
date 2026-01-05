import logging
from langchain.messages import HumanMessage
from langgraph.graph import END
from core.models import HallucinationCheck
from graph.prompts import HALLUCINATION_PROMPT
from graph.common import get_latest_user_question
logger = logging.getLogger(__name__)


def check_hallucination(state, llm):
    """Check if the generated answer is hallucinated."""
    question = get_latest_user_question(state["messages"])
    answer = state["messages"][-1].content
    
    retry_count = state.get("answer_retry_count", 0)

    prompt = HALLUCINATION_PROMPT.format(question=question, answer=answer)
    response = (
        llm
        .with_structured_output(HallucinationCheck)
        .invoke([{"role": "user", "content": prompt}])
    )
    
    hallucination_score = response.hallucination
    logger.info(
        f"Hallucination={hallucination_score} "
        f"(retry_count={retry_count})"
    )
    
    # Check if we've hit the retry limit
    if retry_count >= 2:
        logger.warning(
            "Max hallucination retries reached → accepting current answer"
        )
        return END
    
    if hallucination_score == "yes":
        return "generate_answer"
    else:
        return END

