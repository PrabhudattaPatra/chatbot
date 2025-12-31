from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

def get_websearch_tool():
    """
    Tavily web search tool for real-time CGU-related queries
    (e.g., Twitter/X posts, recent announcements)
    """
    return TavilySearch(
        max_results=5,
        include_raw_content=True,
        search_depth="advanced",
        include_domains=[
            "https://x.com/CguOdisha",
            "https://twitter.com/CguOdisha",
        ],
    )
