from langchain.tools import tool
from tools.retrievers import get_notice_retriever

@tool
def retrieve_notice_board_doc(query: str) -> str:
    """
    Search and return official CGU notice board announcements, including:
    - Academic calendars
    - Timetables
    - Convocation notices
    - Circulars & events
    """
    retriever = get_notice_retriever()
    docs = retriever.invoke(query)

    return "\n\n".join(doc.page_content for doc in docs)
