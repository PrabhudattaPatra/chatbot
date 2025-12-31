from typing_extensions import Annotated
from langgraph.graph import MessagesState

class AgentState(MessagesState):
    rewrite_count: Annotated[int, "Number of question rewrites"] = 0
    answer_retry_count: Annotated[int, "Number of answer regenerations"] = 0
