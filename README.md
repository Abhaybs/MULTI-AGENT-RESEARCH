# AI Research Assistant

An intelligent research assistant powered by LangGraph that automatically researches topics, gathers information from the web, and generates comprehensive reports.

## Features

- 🤖 **AI-Powered Planning**: Automatically breaks down research topics into relevant sections
- 🔍 **Web Search Integration**: Uses Tavily API to gather real-time information from the web
- 📝 **Automated Report Generation**: Compiles research findings into well-structured reports
- 🔄 **Workflow Orchestration**: Uses LangGraph for robust agent coordination

## Architecture

The system uses a three-agent workflow:

1. **Planner Agent**: Analyzes the research topic and breaks it down into 5-7 key sections
2. **Researcher Agent**: For each section, performs web searches and gathers relevant information
3. **Writer Agent**: Compiles all research data into a comprehensive, well-structured report

## Tech Stack

- **LangGraph**: Workflow orchestration
- **Groq**: Fast LLM inference (Llama 3.3 70B)
- **Tavily**: Web search API
- **Python 3.12+**

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd "Research assisstant"
```

2. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install langgraph langchain-groq tavily-python python-dotenv
```

4. Create `.env` file in `backend/` directory:
```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

5. Get your free API keys:
   - Groq: https://console.groq.com/keys
   - Tavily: https://tavily.com

## Usage

Run the research assistant:

```bash
cd backend
python main.py
```

Enter your research topic when prompted, and the system will:
1. Plan the research structure
2. Search the web for each section
3. Generate a comprehensive report

## Project Structure

```
Research assisstant/
├── backend/
│   ├── agents/
│   │   ├── planner.py      # Plans research sections
│   │   ├── research.py     # Performs web searches
│   │   └── writer.py       # Generates final report
│   ├── graph/
│   │   └── workflow.py     # LangGraph workflow definition
│   ├── state/
│   │   └── state.py        # Shared state management
│   ├── tools/
│   │   └── web_search.py   # Tavily web search integration
│   ├── main.py             # Entry point
│   └── .env                # API keys (not in git)
├── venv/                   # Virtual environment (not in git)
├── .gitignore
└── README.md
```

## Example Output

```
Enter research topic: Artificial Intelligence in Healthcare

Running Research Agent...
Researching section: Introduction to AI in Healthcare
Researching section: AI Applications in Medical Diagnosis
...

FINAL REPORT:

[Comprehensive research report with introduction, sections, and conclusion]
```

## License

MIT
