from langchain_groq import ChatGroq
from state.state import ResearchState
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=os.getenv("GROQ_API_KEY"))

def writer_agent(state: ResearchState):

    query = state["query"]
    research_data = state["research_data"]

    compiled_notes = ""

    for section, content in research_data.items():
        compiled_notes += f"\n## {section}\n{content}\n"

    prompt = f"""
    You are an expert research report writer.

    Create a professional research report on:

    {query}

    Using the following research notes and verified sources:

    {compiled_notes}

    Requirements:
    - Use markdown formatting
    - Include clear headings and subheadings
    - Be factual and concise
    - Include bullet points where useful
    - Mention sources naturally
    - Add a final conclusion section
    - Do NOT hallucinate information
    - Use only provided research data
    """

    response = llm.invoke(prompt)

    return {
        "final_report": response.content
    }