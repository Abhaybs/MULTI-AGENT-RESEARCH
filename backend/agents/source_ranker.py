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

def source_ranker_agent(state: ResearchState):

    print("Running Source Ranker Agent...")

    research_data = state["research_data"]
    papers_data = state["papers"]
    extracted_insights = state["extracted_insights"]

    combined_sources = ""
    
    print("\n" + "="*80)
    print("SOURCE RANKER - PROCESSING")
    print("="*80)
    print(f"Ranking sources from {len(research_data)} web research sections")
    print(f"Total papers: {sum(len(p) for p in papers_data.values())}")
    print(f"Insights length: {len(extracted_insights)} chars")
    print("="*80)
    
    max_content_per_section = 600  # Limit content
    max_papers_per_section = 2      # Limit papers
    max_abstract_length = 300       # Limit abstract

    # =========================
    # WEB SOURCES (TRUNCATED)
    # =========================

    for section, content in research_data.items():

        truncated = content[:max_content_per_section]
        if len(content) > max_content_per_section:
            truncated += "\n[...truncated]"

        combined_sources += f"""
SECTION: {section}

WEB RESEARCH:
{truncated}

========================================
"""

    # =========================
    # PAPER SOURCES (LIMITED)
    # =========================

    for section, papers in papers_data.items():

        combined_sources += f"""
SECTION: {section}

ACADEMIC PAPERS:
"""

        for paper in papers[:max_papers_per_section]:
            
            abstract = paper['summary'][:max_abstract_length]
            if len(paper['summary']) > max_abstract_length:
                abstract += "\n[...truncated]"

            combined_sources += f"""

Title: {paper['title']}

Published:
{paper['published']}

Abstract:
{abstract}

PDF:
{paper['pdf_url']}

----------------------------------------
"""

    # =========================
    # RANKING PROMPT
    # =========================

    prompt = f"""
You are an expert AI research evaluator.

Your task is to rank and filter research sources.

Evaluate:
- relevance
- technical depth
- credibility
- usefulness
- research quality

Prioritize:
- academic papers
- official documentation
- technical sources
- research-backed findings

Deprioritize:
- weak blogs
- repetitive information
- shallow explanations
- low-quality sources

Return:
1. Best technical insights
2. Most reliable findings
3. Most relevant papers
4. Important methodologies
5. High-quality summarized research

Keep the output concise and information-dense.

EXTRACTED RESEARCH INSIGHTS:

{extracted_insights}
"""

    response = llm.invoke(prompt)

    print("\n" + "="*80)
    print("SOURCE RANKER - OUTPUT (First 500 chars)")
    print("="*80)
    print(response.content[:500] + "...")
    print("="*80 + "\n")

    print("Source Ranker Completed!")

    return {
        "ranked_sources": response.content
    }