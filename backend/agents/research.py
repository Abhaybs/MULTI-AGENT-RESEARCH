from langchain_groq import ChatGroq
from state.state import ResearchState
from tools.web_search import search_web
from dotenv import load_dotenv
import os
import time
load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=os.getenv("GROQ_API_KEY"))

def researcher_agent(state: ResearchState):

    print("Running Research Agent...")

    sections = state["sections"]
    topic = state["query"]

    research_data = {}

    for section in sections:

        print(f"\nResearching section: {section}")

        search_query = f"{topic} {section}"

        start = time.time()

        web_results = search_web(search_query)

        print(f"Completed in {time.time() - start:.2f} seconds")

        formatted_notes = ""

        for idx, result in enumerate(web_results, start=1):

            formatted_notes += f"""
Result {idx}

Title:
{result['title']}

Content:
{result['content']}

Source URL:
{result['url']}

----------------------------------------
"""

        research_data[section] = formatted_notes

    return {
        "research_data": research_data
    }