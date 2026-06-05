from typing import TypedDict, List, Dict

class ResearchState(TypedDict):
    query: str
    route: str
    sections: List[str]
    research_data: Dict[str, str]
    final_report: str