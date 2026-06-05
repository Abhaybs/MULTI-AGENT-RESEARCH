from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
from state.state import ResearchState

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

def planner_agent(state: ResearchState):

    query = state["query"]

    prompt = f"""
    You are a research planner.

    Break the following topic into 5-7 important research sections.

    Topic:
    {query}

    Return ONLY a Python list.
    """

    response = llm.invoke(prompt)

    sections = eval(response.content)

    return {
        "sections": sections
    }