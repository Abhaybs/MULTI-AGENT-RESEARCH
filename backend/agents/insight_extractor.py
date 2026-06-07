from langchain_groq import ChatGroq
from state.state import ResearchState
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

def insight_extractor_agent(state: ResearchState):

    print("Running Insight Extractor Agent...")

    papers_data = state["papers"]

    compiled_papers = ""
    
    print("\n" + "="*80)
    print("INSIGHT EXTRACTOR - PROCESSING")
    print("="*80)
    print(f"Extracting insights from papers across {len(papers_data)} sections")
    print("="*80)

    # =========================
    # COMPILE PAPERS
    # =========================

    for section, papers in papers_data.items():

        compiled_papers += f"""
SECTION: {section}

"""

        # Limit to 2 papers per section to avoid token limits
        for paper in papers[:2]:
            # Truncate abstract to 300 characters
            abstract = paper['summary'][:300] + "..." if len(paper['summary']) > 300 else paper['summary']

            compiled_papers += f"""
TITLE:
{paper['title']}

ABSTRACT:
{abstract}

PUBLISHED:
{paper['published']}

PDF:
{paper['pdf_url']}

----------------------------------------
"""

    # =========================
    # EXTRACTION PROMPT
    # =========================

    prompt = f"""
You are an expert AI research scientist.

Your task is to extract HIGH-VALUE research insights from academic papers.

For each paper identify:

1. Main Contribution
2. Methodology
3. Key Findings
4. Advantages
5. Limitations
6. Real-world Applications
7. Research Significance

IMPORTANT:
- Keep insights concise
- Avoid repeating abstract text
- Focus on technical meaning
- Extract only the most valuable information
- Use professional research language

Return structured outputs.

ACADEMIC PAPERS:

{compiled_papers}
"""

    response = llm.invoke(prompt)

    print("\n" + "="*80)
    print("INSIGHT EXTRACTOR - OUTPUT (First 500 chars)")
    print("="*80)
    print(response.content[:500] + "...")
    print("="*80 + "\n")

    print("Insight Extractor Completed!")

    return {
        "extracted_insights": response.content
    }