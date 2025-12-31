import logging
from langchain.messages import SystemMessage, HumanMessage

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are summarizing a scanned academic document page "
    "for a Retrieval-Augmented Generation (RAG) system."
)

USER_PROMPT = (
    "Give a detailed, factual summary of this page. "
    "Extract all dates, rules, tables, headings, and instructions. "
    "Do not miss any information."
)

def summarize_image_page(image_base64: str, model) -> str:
    try:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(
                content=[
                    {"type": "text", "text": USER_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        },
                    },
                ]
            ),
        ]

        response = model.invoke(messages)
        return response.content

    except Exception:
        logger.exception("Multimodal summarization failed")
        raise
