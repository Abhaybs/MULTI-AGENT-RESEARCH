from langgraph.graph import StateGraph, START, END

from state.state import ResearchState

from agents.planner import planner_agent
from agents.research import researcher_agent
from agents.writer import writer_agent

builder = StateGraph(ResearchState)

builder.add_node("planner", planner_agent)
builder.add_node("researcher", researcher_agent)
builder.add_node("writer", writer_agent)

builder.add_edge(START, "planner")
builder.add_edge("planner", "researcher")
builder.add_edge("researcher", "writer")
builder.add_edge("writer", END)

graph = builder.compile()