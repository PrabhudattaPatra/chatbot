from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from graph.state import AgentState
from graph.nodes.decision import generate_query_or_respond
from graph.nodes.rewrite import rewrite_question
from graph.nodes.answer import generate_answer
from graph.nodes.grade_docs import grade_documents
from graph.nodes.hallucination import check_hallucination

from tools.blog_tool import retrieve_blog_posts
from tools.exam_tool import retrieve_examination_cell_doc
from tools.notice_tool import retrieve_notice_board_doc
from tools.websearch_tool import get_websearch_tool


def build_graph(llm, checkpointer=None):
    """
    Build and compile the LangGraph workflow.

    Design principles:
    - Graph is built ONCE (FastAPI lifespan)
    - LangGraph nodes accept ONLY `state`
    - `llm` is injected via closures (lambda)
    - Checkpointer enables short-term memory (thread_id)
    """

    # ===============================
    # Tool setup
    # ===============================
    websearch_tool = get_websearch_tool()

    tool_node = ToolNode(
        tools=[
            retrieve_blog_posts,
            retrieve_examination_cell_doc,
            retrieve_notice_board_doc,
            websearch_tool,
        ]
    )

    # ===============================
    # Initialize workflow
    # ===============================
    workflow = StateGraph(AgentState)


    # Define the nodes we will cycle between
    workflow.add_node("generate_query_or_respond",
        lambda s: generate_query_or_respond(s, llm),
    )
    workflow.add_node("retrieve", tool_node)
    workflow.add_node("rewrite_question", lambda s: rewrite_question(s, llm))
    workflow.add_node("generate_answer", lambda s: generate_answer(s, llm))

    workflow.add_edge(START, "generate_query_or_respond")

    # Decide whether to retrieve
    workflow.add_conditional_edges(
        "generate_query_or_respond",
        # Assess LLM decision (call `retriever_tool` tool or respond to the user)
        tools_condition,
        {
            # Translate the condition outputs to nodes in our graph
            "tools": "retrieve",
            END: END,
        },
    )

    # Edges taken after the `action` node is called.
    workflow.add_conditional_edges(
        "retrieve",
        # Assess agent decision
        lambda s: grade_documents(s, llm)
    )
    workflow.add_conditional_edges(
        "generate_answer",
        # Assess agent decision
        lambda s: check_hallucination(s, llm)
    )
    workflow.add_edge("generate_answer", END)
    workflow.add_edge("rewrite_question", "generate_query_or_respond")

    # Compile
    return workflow.compile(checkpointer=checkpointer)
