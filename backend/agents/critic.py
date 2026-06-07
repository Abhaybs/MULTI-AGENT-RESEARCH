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

def critic_agent(state: ResearchState):

    print("Running Critic Agent...")

    ranked_sources = state["ranked_sources"]
    
    print("\n" + "="*80)
    print("CRITIC AGENT - PROCESSING")
    print("="*80)
    print(f"Validating and refining ranked sources ({len(ranked_sources)} chars)")
    print("="*80)

    # =========================
    # CRITIC PROMPT
    # =========================

    prompt = f"""
You are a senior AI research analyst.

Your task is to refine and validate research data.

You are given:
- ranked and filtered research sources
- web research insights
- academic paper summaries

Your job:

1. Remove repetitive information
2. Remove weak or low-quality insights
3. Prioritize academic/research-backed findings
4. Extract the MOST important insights
5. Keep technical accuracy high
6. Organize findings clearly
7. Highlight important methodologies and challenges
8. Keep the output concise but information-dense

Return:
- Key Findings
- Important Research Insights
- Challenges
- Future Directions
- Strong Technical Observations

RANKED RESEARCH DATA:
{ranked_sources}
"""

    response = llm.invoke(prompt)

    print("\n" + "="*80)
    print("CRITIC AGENT - OUTPUT (First 500 chars)")
    print("="*80)
    print(response.content[:500] + "...")
    print("="*80 + "\n")

    print("Critic Agent Completed!")

    return {
        "validated_research": response.content
    }