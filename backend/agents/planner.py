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

    print("\n" + "="*80)
    print("PLANNER AGENT - PROCESSING")
    print("="*80)
    print(f"Query: {query}")
    print("="*80)

    response = llm.invoke(prompt)

    print("\n" + "="*80)
    print("PLANNER AGENT - OUTPUT")
    print("="*80)
    print(response.content)
    print("="*80 + "\n")

    sections = eval(response.content)

    return {
        "sections": sections
    }