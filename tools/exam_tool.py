from langchain.tools import tool
from tools.retrievers import get_exam_retriever

@tool
def retrieve_examination_cell_doc(query: str) -> str:
    """
    Search and return official CGU examination notifications, including:
    - Exam schedules
    - Admit card notices
    - Result announcements
    - Examination circulars
    """
    retriever = get_exam_retriever()
    docs = retriever.invoke(query)

    return "\n\n".join(doc.page_content for doc in docs)
