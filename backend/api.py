from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import asyncio

from graph.workflow import graph

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    query: str

async def research_stream(query: str):
    """Stream research progress to frontend"""
    
    # Send initial status
    yield f"data: {json.dumps({'type': 'log', 'message': f'Starting research on: {query}'})}\n\n"
    await asyncio.sleep(0.1)  # Small delay to ensure delivery
    
    # Update planner status
    yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'planner', 'status': 'running'})}\n\n"
    await asyncio.sleep(0.1)
    yield f"data: {json.dumps({'type': 'log', 'message': 'Planner Agent: Breaking down research topic...'})}\n\n"
    await asyncio.sleep(0.1)
    
    try:
        # Run the graph
        result = {}
        for event in graph.stream({"query": query}):
            # Extract node name and data
            node_name = list(event.keys())[0]
            node_data = event[node_name]
            
            if node_name == "planner":
                sections = node_data.get("sections", [])
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'planner', 'status': 'completed'})}\n\n"
                await asyncio.sleep(0.1)
                yield f"data: {json.dumps({'type': 'log', 'message': f'Planner Agent: Created {len(sections)} research sections'})}\n\n"
                await asyncio.sleep(0.1)
                
                # Start researcher
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'researcher', 'status': 'running'})}\n\n"
                await asyncio.sleep(0.1)
                yield f"data: {json.dumps({'type': 'log', 'message': 'Research Agent: Searching web for each section...'})}\n\n"
                await asyncio.sleep(0.1)
                
            elif node_name == "researcher":
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'researcher', 'status': 'completed'})}\n\n"
                await asyncio.sleep(0.1)
                yield f"data: {json.dumps({'type': 'log', 'message': 'Research Agent: Completed web research'})}\n\n"
                await asyncio.sleep(0.1)
                
                # Start paper analyzer
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'paper_analyzer', 'status': 'running'})}\n\n"
                await asyncio.sleep(0.1)
                yield f"data: {json.dumps({'type': 'log', 'message': 'Paper Analyzer: Searching arXiv for academic papers...'})}\n\n"
                await asyncio.sleep(0.1)
                
            elif node_name == "paper_analyzer":
                papers_data = node_data.get("papers", {})
                total_papers = sum(len(papers) for papers in papers_data.values())
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'paper_analyzer', 'status': 'completed'})}\n\n"
                await asyncio.sleep(0.1)
                yield f"data: {json.dumps({'type': 'log', 'message': f'Paper Analyzer: Found {total_papers} relevant papers from arXiv'})}\n\n"
                await asyncio.sleep(0.1)
                
                # Start insight extractor
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'insight_extractor', 'status': 'running'})}\n\n"
                await asyncio.sleep(0.1)
                yield f"data: {json.dumps({'type': 'log', 'message': 'Insight Extractor: Extracting high-value research insights from papers...'})}\n\n"
                await asyncio.sleep(0.1)
                
            elif node_name == "insight_extractor":
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'insight_extractor', 'status': 'completed'})}\n\n"
                await asyncio.sleep(0.1)
                yield f"data: {json.dumps({'type': 'log', 'message': 'Insight Extractor: Research insights extracted from academic papers'})}\n\n"
                await asyncio.sleep(0.1)
                
                # Start source ranker
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'source_ranker', 'status': 'running'})}\n\n"
                await asyncio.sleep(0.1)
                yield f"data: {json.dumps({'type': 'log', 'message': 'Source Ranker: Evaluating and ranking sources by quality...'})}\n\n"
                await asyncio.sleep(0.1)
                
            elif node_name == "source_ranker":
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'source_ranker', 'status': 'completed'})}\n\n"
                await asyncio.sleep(0.1)
                yield f"data: {json.dumps({'type': 'log', 'message': 'Source Ranker: Sources ranked and filtered by quality'})}\n\n"
                await asyncio.sleep(0.1)
                
                # Start critic
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'critic', 'status': 'running'})}\n\n"
                await asyncio.sleep(0.1)
                yield f"data: {json.dumps({'type': 'log', 'message': 'Critic Agent: Validating and refining research data...'})}\n\n"
                await asyncio.sleep(0.1)
                
            elif node_name == "critic":
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'critic', 'status': 'completed'})}\n\n"
                await asyncio.sleep(0.1)
                yield f"data: {json.dumps({'type': 'log', 'message': 'Critic Agent: Research validated and refined'})}\n\n"
                await asyncio.sleep(0.1)
                
                # Start writer
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'writer', 'status': 'running'})}\n\n"
                await asyncio.sleep(0.1)
                yield f"data: {json.dumps({'type': 'log', 'message': 'Writer Agent: Compiling final report with validated data...'})}\n\n"
                await asyncio.sleep(0.1)
                
            elif node_name == "writer":
                final_report = node_data.get("final_report", "")
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'writer', 'status': 'completed'})}\n\n"
                await asyncio.sleep(0.1)
                yield f"data: {json.dumps({'type': 'log', 'message': 'Writer Agent: Report generated successfully!'})}\n\n"
                await asyncio.sleep(0.1)
                
                # Start citation agent
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'citation_agent', 'status': 'running'})}\n\n"
                await asyncio.sleep(0.1)
                yield f"data: {json.dumps({'type': 'log', 'message': 'Citation Agent: Adding inline citations and references...'})}\n\n"
                await asyncio.sleep(0.1)
                
            elif node_name == "citation_agent":
                cited_report = node_data.get("cited_report", "")
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'citation_agent', 'status': 'completed'})}\n\n"
                await asyncio.sleep(0.1)
                yield f"data: {json.dumps({'type': 'log', 'message': 'Citation Agent: Citations added successfully!'})}\n\n"
                await asyncio.sleep(0.1)
                yield f"data: {json.dumps({'type': 'final_report', 'report': cited_report})}\n\n"
                await asyncio.sleep(0.1)
                
                result = node_data
        
        yield f"data: {json.dumps({'type': 'log', 'message': 'Research completed!'})}\n\n"
        
    except Exception as e:
        yield f"data: {json.dumps({'type': 'log', 'message': f'Error: {str(e)}'})}\n\n"

@app.post("/research")
async def research(request: ResearchRequest):
    """Stream research progress"""
    return StreamingResponse(
        research_stream(request.query),
        media_type="text/event-stream"
    )

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
