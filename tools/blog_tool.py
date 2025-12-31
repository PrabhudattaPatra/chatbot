from langchain.tools import tool
from tools.retrievers import get_static_retriever

@tool
def retrieve_blog_posts(query: str) -> str:
    """
    Search and return official CGU university information, including:
    - Admissions & eligibility
    - Fee structure & payments
    - Scholarships & loans
    - Campus facilities & policies
    - Placements & recruiters
    """
    retriever = get_static_retriever()
    docs = retriever.invoke(query)

    return "\n\n".join(doc.page_content for doc in docs)
