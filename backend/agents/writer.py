from langchain_groq import ChatGroq
from state.state import ResearchState
from dotenv import load_dotenv
import os
import re

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

def writer_agent(state: ResearchState):

    print("Running Writer Agent...")

    query = state["query"]

    # Use validated research from critic agent
    validated_research = state["validated_research"]

    # Raw data (only for references extraction)
    research_data = state["research_data"]
    papers_data = state.get("papers", {})
    
    print("\n" + "="*80)
    print("WRITER AGENT - PROCESSING")
    print("="*80)
    print(f"Topic: {query}")
    print(f"Validated research length: {len(validated_research)} chars")
    print("="*80)

    # =========================
    # GATHER REFERENCES
    # =========================

    references = []

    # Extract URLs from web research
    for section, content in research_data.items():

        urls = re.findall(r'https?://[^\s\)\]]+', content)

        for url in urls[:3]:

            cleaned_url = url.strip().rstrip('.,;')

            if cleaned_url not in references:
                references.append(cleaned_url)

    # Add paper PDF URLs
    max_papers_per_section = 3

    for section, papers in papers_data.items():

        for paper in papers[:max_papers_per_section]:

            pdf_url = paper.get("pdf_url")

            if pdf_url and pdf_url not in references:
                references.append(pdf_url)

    # Limit total references
    references = references[:25]

    # =========================
    # FINAL PROMPT
    # =========================

    prompt = f"""
You are an expert AI research analyst and technical report writer.

Create a professional, technical, and well-structured research report on:

{query}

You are provided with validated research generated from:
- real-time web research
- academic papers from arXiv
- research refinement and filtering

=========================
VALIDATED RESEARCH
=========================

{validated_research}

=========================
REFERENCES
=========================

{chr(10).join([f"{i+1}. {url}" for i, url in enumerate(references)])}

=========================
REPORT REQUIREMENTS
=========================

- Use markdown formatting
- Create proper headings and subheadings
- Write in a professional research style
- Avoid repetition
- Include:
    - introduction
    - key findings
    - technical insights
    - challenges/limitations
    - future directions
    - conclusion
- Use concise but information-dense writing
- Prioritize academic/research-backed findings
- Mention important methodologies if relevant
- Avoid hallucinations
- Use ONLY provided validated research

IMPORTANT:
At the END of the report, create a:

## References

section using the provided URLs.
"""

    response = llm.invoke(prompt)

    print("\n" + "="*80)
    print("WRITER AGENT - FINAL REPORT GENERATED")
    print("="*80)
    print(f"Report length: {len(response.content)} chars")
    print(f"Total references: {len(references)}")
    print("="*80 + "\n")

    print("Writer Agent Completed!")

    return {
        "final_report": response.content
    }