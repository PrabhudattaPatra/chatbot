from tools.blog_tool import retrieve_blog_posts
from tools.exam_tool import retrieve_examination_cell_doc
from tools.notice_tool import retrieve_notice_board_doc
from tools.websearch_tool import get_websearch_tool

def generate_query_or_respond(state, llm):
    """Call the model to generate a response based on the current state. Given
    the question, it will decide to retrieve using the retriever_tool,examination_cell_retriever,notice_board_doc
    websearch_tool or simply respond to the user.
    """

    websearch_tool = get_websearch_tool()
    response = (
        llm
        .bind_tools([
            retrieve_blog_posts,
            retrieve_examination_cell_doc,
            retrieve_notice_board_doc,
            websearch_tool,
        ])
        .invoke(state["messages"])
    )

    return {"messages": [response]}
