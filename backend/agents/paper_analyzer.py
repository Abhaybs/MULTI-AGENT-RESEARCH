from state.state import ResearchState
from tools.paper_search import search_papers

def paper_analyzer_agent(state: ResearchState):

    print("Running Paper Analyzer Agent...")

    sections = state["sections"]
    
    print("\n" + "="*80)
    print("PAPER ANALYZER - PROCESSING")
    print("="*80)
    print(f"Searching papers for {len(sections)} sections")
    print("="*80)

    papers_data = {}

    for section in sections:

        print(f"Searching papers for: {section}")

        papers = search_papers(section)

        papers_data[section] = papers

    return {
        "papers": papers_data
    }