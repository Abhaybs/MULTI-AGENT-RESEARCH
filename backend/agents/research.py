from langchain_groq import ChatGroq
from state.state import ResearchState
from tools.web_search import search_web
from dotenv import load_dotenv
import os
import time
load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=os.getenv("GROQ_API_KEY"))

def research_section(topic, section):
    """Synchronous version for compatibility with LangGraph"""
    print(f"Researching: {section}")

    search_query = f"{topic} {section}"

    web_results = search_web(search_query)

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

    return section, formatted_notes


def researcher_agent(state: ResearchState):

    print("Running Concurrent Research Agent...")

    sections = state["sections"]
    topic = state["query"]

    # Use concurrent.futures for parallel execution instead of asyncio
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    research_data = {}
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit all research tasks
        future_to_section = {
            executor.submit(research_section, topic, section): section
            for section in sections
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_section):
            section, notes = future.result()
            research_data[section] = notes

    return {
        "research_data": research_data
    }