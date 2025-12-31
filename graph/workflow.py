from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from graph.state import AgentState
from graph.nodes.decision import generate_query_or_respond
from graph.nodes.grade_docs import grade_documents
from graph.nodes.rewrite import rewrite_question
from graph.nodes.answer import generate_answer
from graph.nodes.hallucination import check_hallucination

from tools.blog_tool import retrieve_blog_posts
from tools.exam_tool import retrieve_examination_cell_doc
from tools.notice_tool import retrieve_notice_board_doc
from tools.websearch_tool import get_websearch_tool

def build_graph(llm, checkpointer=None):
    workflow = StateGraph(AgentState)

    workflow.add_node(
        "decision",
        lambda s: generate_query_or_respond(s, llm),
    )

    workflow.add_node(
        "retrieve",
        ToolNode([
            retrieve_blog_posts,
            retrieve_examination_cell_doc,
            retrieve_notice_board_doc,
            get_websearch_tool(),
        ]),
    )

    workflow.add_node(
        "rewrite_question",
        lambda s: rewrite_question(s, llm),
    )

    workflow.add_node(
        "generate_answer",
        lambda s: generate_answer(s, llm),
    )

    workflow.add_node(
        "check_hallucination",
        lambda s: check_hallucination(s, llm),
    )

    workflow.add_edge(START, "decision")

    workflow.add_conditional_edges(
        "decision",
        tools_condition,
        {"tools": "retrieve", END: END},
    )

    workflow.add_conditional_edges(
        "retrieve",
        grade_documents,
    )

    workflow.add_conditional_edges(
        "generate_answer",
        check_hallucination,
    )

    workflow.add_edge("rewrite_question", "decision")
    workflow.add_edge("generate_answer", END)

    return workflow.compile(checkpointer=checkpointer)
