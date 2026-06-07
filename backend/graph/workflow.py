from langgraph.graph import StateGraph, START, END
from agents.paper_analyzer import paper_analyzer_agent
from state.state import ResearchState
from agents.critic import critic_agent
from agents.planner import planner_agent
from agents.research import researcher_agent
from agents.writer import writer_agent
from agents.source_ranker import source_ranker_agent
from agents.insight_extractor import insight_extractor_agent
from agents.citation_agent import citation_agent

builder = StateGraph(ResearchState)

builder.add_node("planner", planner_agent)
builder.add_node("researcher", researcher_agent)
builder.add_node("paper_analyzer", paper_analyzer_agent)
builder.add_node("insight_extractor", insight_extractor_agent)
builder.add_node("source_ranker", source_ranker_agent)
builder.add_node("critic", critic_agent)
builder.add_node("writer", writer_agent)
builder.add_node("citation_agent", citation_agent)


builder.add_edge(START, "planner")
builder.add_edge("planner", "researcher")
builder.add_edge("researcher", "paper_analyzer")
builder.add_edge("paper_analyzer", "insight_extractor")
builder.add_edge("insight_extractor", "source_ranker")
builder.add_edge("source_ranker", "critic")
builder.add_edge("critic", "writer")
builder.add_edge("writer", "citation_agent")
builder.add_edge("citation_agent", END)

graph = builder.compile()
print(graph.get_graph().draw_ascii())