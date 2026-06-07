from typing import TypedDict, List, Dict

class ResearchState(TypedDict):
    query: str
    route: str
    sections: List[str]
    research_data: Dict[str, str]
    papers: Dict[str, list]
    extracted_insights: str
    ranked_sources: str
    validated_research: str
    final_report: str
    cited_report: str