from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()

def get_llm():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY não encontrada no ambiente.")

    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,       
        max_tokens=2048,
        api_key=api_key,
    )