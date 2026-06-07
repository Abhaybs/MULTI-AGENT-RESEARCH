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

def citation_agent(state: ResearchState):

    print("Running Citation Agent...")

    report = state["final_report"]

    papers_data = state.get("papers", {})
    research_data = state.get("research_data", {})
    
    print("\n" + "="*80)
    print("CITATION AGENT - PROCESSING")
    print("="*80)
    print(f"Adding citations to report ({len(report)} chars)")
    print(f"Available sources: {len(papers_data)} paper sections, {len(research_data)} web sections")
    print("="*80)

    # =========================
    # BUILD SOURCE LIST
    # =========================

    sources = []

    # Add paper URLs
    for section, papers in papers_data.items():

        for paper in papers[:3]:

            sources.append({
                "title": paper["title"],
                "url": paper["pdf_url"]
            })

    # Add web URLs
    import re

    for section, content in research_data.items():

        urls = re.findall(r'https?://[^\s\)\]]+', content)

        for url in urls[:2]:

            sources.append({
                "title": "Web Source",
                "url": url
            })

    # Remove duplicates
    unique_sources = []

    seen = set()

    for source in sources:

        if source["url"] not in seen:

            unique_sources.append(source)

            seen.add(source["url"])

    # Limit citations
    unique_sources = unique_sources[:20]

    # =========================
    # FORMAT REFERENCES
    # =========================

    # Use proper markdown line breaks (two spaces + newline)
    formatted_references = "\n"

    for idx, source in enumerate(unique_sources, start=1):
        formatted_references += f"[{idx}] {source['title']}  \n{source['url']}\n\n"

    # =========================
    # CITATION PROMPT
    # =========================

    prompt = f"""
You are an expert academic editor.

Your task is to enhance the following research report by:

1. Adding inline citations where relevant (use format: [1], [2], [3])
2. Maintaining readability
3. Preserving technical quality
4. Adding a properly formatted References section at the end
5. Ensuring citations align with claims

IMPORTANT RULES:
- Do NOT invent citations
- Use ONLY provided references
- Keep the report professional
- Add citations naturally using [number] format
- Keep markdown formatting intact

CRITICAL FORMATTING REQUIREMENT FOR REFERENCES SECTION:
The References section MUST use this EXACT format - YOU MUST put each reference on separate lines with proper line breaks using two spaces and newline (markdown format):

## References

[1] AR-RAG: Autoregressive Retrieval Augmentation for Image Generation  
https://arxiv.org/pdf/2506.06962v3

[2] Intelligent Human-Machine Interaction Strategies  
https://arxiv.org/pdf/2504.13684v1

[3] Factually: Exploring Wearable Fact-Checking  
https://arxiv.org/pdf/2504.17020v1

IMPORTANT: Each URL must be on its OWN LINE (use two spaces before newline in markdown).  
DO NOT put everything on one long line.  
Each [number] Title should be followed by TWO SPACES, then a newline, then the URL on the next line.

=========================
REPORT
=========================

{report}

=========================
AVAILABLE REFERENCES (USE THESE NUMBERS)
=========================

{formatted_references}

REMINDER: Format references EXACTLY as shown in the example above - each on separate lines with proper markdown line breaks (two spaces + newline)!
"""

    response = llm.invoke(prompt)

    print("\n" + "="*80)
    print("CITATION AGENT - OUTPUT")
    print("="*80)
    print(f"Cited report length: {len(response.content)} chars")
    print(f"Total references: {len(unique_sources)}")
    print("="*80 + "\n")

    print("Citation Agent Completed!")

    return {
        "cited_report": response.content
    }