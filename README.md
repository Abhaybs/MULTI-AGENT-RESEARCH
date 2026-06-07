# AI Research Assistant

An intelligent multi-agent research assistant powered by LangGraph that automatically researches topics, gathers information from academic papers and the web, and generates comprehensive reports with proper citations.

## 🌟 Features

- 🤖 **8-Agent AI System**: Sophisticated multi-agent workflow for high-quality research
- 🔍 **Multi-Source Research**: Combines web search (Tavily) and academic papers (arXiv)
- 📚 **Academic Citations**: Automatic inline citations and reference formatting
- 🎯 **Quality Validation**: Multiple validation layers for reliable research
- ⚡ **Parallel Processing**: Concurrent web searches for faster results
- 🎨 **Modern UI**: Real-time status updates with Next.js frontend
- 📊 **Live Monitoring**: Watch all agents process data in real-time

## 🏗️ Architecture

### 8-Agent Workflow

```
┌─────────┐   ┌──────────┐   ┌────────────┐   ┌──────────────┐
│ Planner │──▶│Researcher│──▶│Paper       │──▶│Insight       │
└─────────┘   └──────────┘   │Analyzer    │   │Extractor     │
                              └────────────┘   └──────────────┘
                                     │                 │
                                     ▼                 ▼
┌────────────┐   ┌────────┐   ┌────────────┐   ┌──────────┐
│Citation    │◀──│Writer  │◀──│Critic      │◀──│Source    │
│Agent       │   └────────┘   └────────────┘   │Ranker    │
└────────────┘                                  └──────────┘
```

### Agent Responsibilities

1. **Planner Agent**: Breaks down research topic into 5-7 strategic sections
2. **Researcher Agent**: Performs parallel web searches using Tavily (5 results per section)
3. **Paper Analyzer Agent**: Searches arXiv for relevant academic papers (5 per section)
4. **Insight Extractor Agent**: Extracts key insights, methodologies, and findings from papers
5. **Source Ranker Agent**: Ranks and filters sources by quality, credibility, and relevance
6. **Critic Agent**: Validates research, removes weak insights, prioritizes academic findings
7. **Writer Agent**: Compiles comprehensive report from validated research
8. **Citation Agent**: Adds inline citations [1], [2] and formatted references section

## 🛠️ Tech Stack

### Backend
- **LangGraph**: Multi-agent workflow orchestration
- **Groq**: Fast LLM inference (Llama 3.3 70B Versatile)
- **Tavily**: AI-optimized web search API
- **arXiv API**: Academic paper retrieval
- **FastAPI**: SSE streaming backend
- **Python 3.12+**

### Frontend
- **Next.js 16**: React framework
- **TypeScript**: Type-safe development
- **Tailwind CSS v4**: Modern styling
- **Server-Sent Events (SSE)**: Real-time updates
- **React Markdown**: Report rendering

## 📋 Prerequisites

- Python 3.12 or higher
- Node.js 18+ and npm
- Git

## 🚀 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Abhaybs/MULTI-AGENT-RESEARCH.git
cd "Research assisstant"
```

### 2. Backend Setup

```bash
# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Install Python dependencies
pip install langgraph langchain-groq tavily-python python-dotenv arxiv fastapi uvicorn
```

### 3. Frontend Setup

```bash
cd frontend
npm install
cd ..
```

### 4. Environment Variables

Create `backend/.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 5. Get Free API Keys

- **Groq**: https://console.groq.com/keys (100,000 tokens/day free)
- **Tavily**: https://tavily.com (1,000 searches/month free)

## 💻 Usage

### Start Backend Server

```bash
cd backend
python api.py
```

Backend runs on: `http://localhost:8000`

### Start Frontend Server

```bash
cd frontend
npm run dev
```

Frontend runs on: `http://localhost:3000`

### Use the Application

1. Open http://localhost:3000 in your browser
2. Enter a research topic (e.g., "Quantum Computing Applications")
3. Watch the 8 agents work in real-time
4. View the final report with inline citations and references

## 📁 Project Structure

```
Research assisstant/
├── backend/
│   ├── agents/
│   │   ├── planner.py              # Research planning
│   │   ├── research.py             # Parallel web search
│   │   ├── paper_analyzer.py       # arXiv paper search
│   │   ├── insight_extractor.py    # Extract paper insights
│   │   ├── source_ranker.py        # Rank source quality
│   │   ├── critic.py               # Validate research
│   │   ├── writer.py               # Generate report
│   │   └── citation_agent.py       # Add citations
│   ├── graph/
│   │   └── workflow.py             # LangGraph workflow
│   ├── state/
│   │   └── state.py                # Shared state
│   ├── tools/
│   │   ├── web_search.py           # Tavily integration
│   │   └── paper_search.py         # arXiv integration
│   ├── api.py                      # FastAPI + SSE
│   ├── main.py                     # CLI entry point
│   └── .env                        # API keys (gitignored)
├── frontend/
│   ├── app/
│   │   ├── page.tsx                # Main UI component
│   │   ├── layout.tsx              # App layout
│   │   └── globals.css             # Tailwind styles
│   ├── components/
│   │   └── ui/                     # UI components
│   ├── package.json
│   └── tsconfig.json
├── .gitignore
└── README.md
```

## 📊 Performance

- **Execution Time**: ~30-40 seconds per research report
- **Token Usage**: ~100,000 tokens per report (7 sections × 8 agents)
- **Papers Analyzed**: ~35 papers per research topic
- **Web Sources**: ~35 web results per topic
- **Parallel Processing**: 7× faster research vs sequential

## 🔧 Configuration

### Reduce Token Usage

Edit agent files to reduce limits:

```python
# In insight_extractor.py, source_ranker.py, critic.py
max_papers_per_section = 2  # Reduce from 3
max_abstract_length = 300   # Reduce from 400
```

### Change Number of Sections

Edit `planner.py`:

```python
prompt = f"""
Break the following topic into 5 important research sections.  # Change from 7
```

### Switch LLM Model

For faster/cheaper processing, change in all agent files:

```python
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # Smaller, faster model
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)
```

## 📝 Example Output

### Input
```
Research Topic: Deep Learning Applications
```

### Output Report Structure
```markdown
# Introduction to Deep Learning

Deep learning is a subset of machine learning that involves... [12], [13].
Recent research has made significant advancements [1], [2].

## Key Findings

- Evidential deep learning frameworks [3]
- Mathematical analysis techniques [2]
- Hypercomplex-valued CNNs [8]

## Technical Insights

[Detailed technical content with inline citations]

## References

[1] Learn to Accumulate Evidence from All Training Samples
https://arxiv.org/pdf/2306.11113v2

[2] The Modern Mathematics of Deep Learning
https://arxiv.org/pdf/2105.04026v2

[3] Deep Learning and Computational Physics
https://arxiv.org/pdf/2301.00942v1
```

## 🐛 Troubleshooting

### Rate Limit Error

**Issue**: `groq.RateLimitError: Rate limit reached`

**Solution**: 
- Wait for rate limit reset (shown in error message)
- Create a new Groq API key from another account
- Switch to smaller model (`llama-3.1-8b-instant`)

### Frontend Not Loading

**Issue**: Frontend shows blank page

**Solution**:
```bash
cd frontend
rm -rf .next node_modules
npm install
npm run dev
```

### Backend Connection Error

**Issue**: `Error connecting to backend`

**Solution**:
- Check backend is running on port 8000
- Verify no CORS errors in browser console
- Restart both servers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - feel free to use this project for learning and development!

## 🙏 Acknowledgments

- **LangGraph** for workflow orchestration
- **Groq** for fast LLM inference
- **Tavily** for AI-optimized search
- **arXiv** for open access to research papers

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

⭐ Star this repo if you find it helpful!
