from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import asyncio
from datetime import datetime

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

def get_timestamp():
    """Get formatted timestamp for logs"""
    return datetime.now().strftime("%H:%M:%S")

async def send_log(message: str, level: str = "info"):
    """Helper to format and send log messages with timestamps"""
    timestamp = get_timestamp()
    log_data = {
        'type': 'log',
        'message': message,
        'timestamp': timestamp,
        'level': level  # info, success, warning, error
    }
    return f"data: {json.dumps(log_data)}\n\n"

async def research_stream(query: str):
    """Stream research progress to frontend with detailed real-time logs"""
    
    # Send initial status
    yield await send_log(f'🚀 Starting research on: "{query}"', 'info')
    await asyncio.sleep(0.1)
    
    # Update planner status
    yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'planner', 'status': 'running'})}\n\n"
    await asyncio.sleep(0.1)
    yield await send_log('🧠 Planner Agent: Breaking down research topic into sections...', 'info')
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
                yield await send_log(f'✅ Planner Agent: Generated {len(sections)} research sections', 'success')
                await asyncio.sleep(0.1)
                
                # Log each section
                for i, section in enumerate(sections, 1):
                    yield await send_log(f'   📋 Section {i}: {section}', 'info')
                    await asyncio.sleep(0.05)
                
                # Start researcher
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'researcher', 'status': 'running'})}\n\n"
                await asyncio.sleep(0.1)
                yield await send_log(f'🔍 Research Agent: Starting web research for {len(sections)} sections...', 'info')
                await asyncio.sleep(0.1)
                
            elif node_name == "researcher":
                research_data = node_data.get("research_data", {})
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'researcher', 'status': 'completed'})}\n\n"
                await asyncio.sleep(0.1)
                yield await send_log(f'✅ Research Agent: Completed web research for {len(research_data)} sections', 'success')
                await asyncio.sleep(0.1)
                
                # Start paper analyzer
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'paper_analyzer', 'status': 'running'})}\n\n"
                await asyncio.sleep(0.1)
                yield await send_log('📖 Paper Analyzer: Searching arXiv for academic papers...', 'info')
                await asyncio.sleep(0.1)
                
            elif node_name == "paper_analyzer":
                papers_data = node_data.get("papers", {})
                total_papers = sum(len(papers) for papers in papers_data.values())
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'paper_analyzer', 'status': 'completed'})}\n\n"
                await asyncio.sleep(0.1)
                yield await send_log(f'✅ Paper Analyzer: Found {total_papers} academic papers across {len(papers_data)} sections', 'success')
                await asyncio.sleep(0.1)
                
                # Start insight extractor
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'insight_extractor', 'status': 'running'})}\n\n"
                await asyncio.sleep(0.1)
                yield await send_log('✨ Insight Extractor: Extracting key research insights from papers...', 'info')
                await asyncio.sleep(0.1)
                
            elif node_name == "insight_extractor":
                insights = node_data.get("extracted_insights", {})
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'insight_extractor', 'status': 'completed'})}\n\n"
                await asyncio.sleep(0.1)
                yield await send_log(f'✅ Insight Extractor: Extracted insights from {len(insights)} sections', 'success')
                await asyncio.sleep(0.1)
                
                # Start source ranker
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'source_ranker', 'status': 'running'})}\n\n"
                await asyncio.sleep(0.1)
                yield await send_log('🔧 Source Ranker: Evaluating and ranking sources by quality...', 'info')
                await asyncio.sleep(0.1)
                
            elif node_name == "source_ranker":
                ranked = node_data.get("ranked_sources", {})
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'source_ranker', 'status': 'completed'})}\n\n"
                await asyncio.sleep(0.1)
                yield await send_log(f'✅ Source Ranker: Ranked and filtered {len(ranked)} sections by quality', 'success')
                await asyncio.sleep(0.1)
                
                # Start critic
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'critic', 'status': 'running'})}\n\n"
                await asyncio.sleep(0.1)
                yield await send_log('🛡️ Critic Agent: Validating and refining research data...', 'info')
                await asyncio.sleep(0.1)
                
            elif node_name == "critic":
                validated = node_data.get("validated_research", {})
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'critic', 'status': 'completed'})}\n\n"
                await asyncio.sleep(0.1)
                yield await send_log(f'✅ Critic Agent: Validated and refined {len(validated)} sections', 'success')
                await asyncio.sleep(0.1)
                
                # Start writer
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'writer', 'status': 'running'})}\n\n"
                await asyncio.sleep(0.1)
                yield await send_log('✍️ Writer Agent: Generating comprehensive research report...', 'info')
                await asyncio.sleep(0.1)
                
            elif node_name == "writer":
                final_report = node_data.get("final_report", "")
                word_count = len(final_report.split())
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'writer', 'status': 'completed'})}\n\n"
                await asyncio.sleep(0.1)
                yield await send_log(f'✅ Writer Agent: Generated report with ~{word_count} words', 'success')
                await asyncio.sleep(0.1)
                
                # Start citation agent
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'citation_agent', 'status': 'running'})}\n\n"
                await asyncio.sleep(0.1)
                yield await send_log('💬 Citation Agent: Adding inline citations and references...', 'info')
                await asyncio.sleep(0.1)
                
            elif node_name == "citation_agent":
                cited_report = node_data.get("cited_report", "")
                # Count citations in format [1], [2], etc.
                import re
                citations = re.findall(r'\[\d+\]', cited_report)
                unique_citations = len(set(citations))
                
                yield f"data: {json.dumps({'type': 'agent_status', 'agent': 'citation_agent', 'status': 'completed'})}\n\n"
                await asyncio.sleep(0.1)
                yield await send_log(f'✅ Citation Agent: Added {unique_citations} unique citations to report', 'success')
                await asyncio.sleep(0.1)
                yield f"data: {json.dumps({'type': 'final_report', 'report': cited_report})}\n\n"
                await asyncio.sleep(0.1)
                
                result = node_data
        
        yield await send_log('🎉 Research completed successfully!', 'success')
        
    except Exception as e:
        yield await send_log(f'❌ Error: {str(e)}', 'error')

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
