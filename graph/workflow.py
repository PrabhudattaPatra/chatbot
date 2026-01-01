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

    # ===============================
    # Add nodes (llm injected via lambda)
    # ===============================
    workflow.add_node(
        "generate_query_or_respond",
        lambda s: generate_query_or_respond(s, llm),
    )

    workflow.add_node(
        "retrieve",
        tool_node,
    )

    workflow.add_node(
        "rewrite_question",
        lambda s: rewrite_question(s, llm),
    )

    workflow.add_node(
        "generate_answer",
        lambda s: generate_answer(s, llm),
    )

    # ===============================
    # Entry point
    # ===============================
    workflow.add_edge(START, "generate_query_or_respond")

    # ===============================
    # Decide whether to call tools
    # ===============================
    workflow.add_conditional_edges(
        "generate_query_or_respond",
        tools_condition,
        {
            "tools": "retrieve",
            END: END,
        },
    )

    # ===============================
    # Grade retrieved documents
    # ===============================
    workflow.add_conditional_edges(
        "retrieve",
        lambda s: grade_documents(s, llm),
        {
            "generate_answer": "generate_answer",
            "rewrite_question": "rewrite_question",
        },
    )

    # ===============================
    # Rewrite → back to decision
    # ===============================
    workflow.add_edge("rewrite_question", "generate_query_or_respond")

    # ===============================
    # Hallucination check after answer
    # ===============================
    workflow.add_conditional_edges(
        "generate_answer",
        lambda s: check_hallucination(s, llm),
        {
            END: END,
            "rewrite_question": "rewrite_question",
        },
    )

    # ===============================
    # Compile graph
    # ===============================
    return workflow.compile(checkpointer=checkpointer)
