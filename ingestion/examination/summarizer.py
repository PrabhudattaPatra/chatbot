from langchain_google_genai import ChatGoogleGenerativeAI
from core.config import VISION_MODEL_NAME

def get_exam_summarizer():
    return ChatGoogleGenerativeAI(model=VISION_MODEL_NAME)
