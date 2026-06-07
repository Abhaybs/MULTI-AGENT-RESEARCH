"use client";

import { useState } from "react";
import { Send, CheckCircle2, Loader2, FileText } from "lucide-react";
import ReactMarkdown from "react-markdown";

type AgentStatus = "idle" | "running" | "completed";

interface AgentState {
  planner: AgentStatus;
  researcher: AgentStatus;
  paper_analyzer: AgentStatus;
  insight_extractor: AgentStatus;
  source_ranker: AgentStatus;
  critic: AgentStatus;
  writer: AgentStatus;
  citation_agent: AgentStatus;
}

export default function Home() {
  const [query, setQuery] = useState("");
  const [logs, setLogs] = useState<string[]>([]);
  const [agents, setAgents] = useState<AgentState>({
    planner: "idle",
    researcher: "idle",
    paper_analyzer: "idle",
    insight_extractor: "idle",
    source_ranker: "idle",
    critic: "idle",
    writer: "idle",
    citation_agent: "idle",
  });
  const [finalReport, setFinalReport] = useState("");
  const [isResearching, setIsResearching] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsResearching(true);
    setLogs([]);
    setFinalReport("");
    setAgents({ planner: "idle", researcher: "idle", paper_analyzer: "idle", insight_extractor: "idle", source_ranker: "idle", critic: "idle", writer: "idle", citation_agent: "idle" });

    try {
      const response = await fetch("http://localhost:8000/research", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (reader) {
        let buffer = "";
        
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split("\n\n");
          
          // Keep the last incomplete line in the buffer
          buffer = lines.pop() || "";

          for (const line of lines) {
            if (line.startsWith("data: ")) {
              try {
                const jsonStr = line.slice(6).trim();
                if (jsonStr) {
                  const data = JSON.parse(jsonStr);

                  if (data.type === "agent_status") {
                    console.log("Agent status update:", data.agent, data.status);
                    setAgents((prev) => ({
                      ...prev,
                      [data.agent]: data.status,
                    }));
                  } else if (data.type === "log") {
                    console.log("Log:", data.message);
                    setLogs((prev) => [...prev, data.message]);
                  } else if (data.type === "final_report") {
                    console.log("Final report received");
                    setFinalReport(data.report);
                  }
                }
              } catch (e) {
                console.error("Error parsing SSE message:", e, line);
              }
            }
          }
        }
      }
    } catch (error) {
      console.error("Error:", error);
      setLogs((prev) => [...prev, "Error connecting to backend"]);
    } finally {
      setIsResearching(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-gray-100">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <header className="mb-12 text-center">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
            AI Research Assistant
          </h1>
          <p className="text-gray-400">
            Powered by LangGraph • Real-time Web Research
          </p>
        </header>

        {/* Input Box */}
        <div className="mb-8">
          <form onSubmit={handleSubmit} className="relative">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter research topic..."
              className="w-full bg-gray-900 border border-gray-800 rounded-lg px-6 py-4 pr-14 text-gray-100 placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors"
              disabled={isResearching}
            />
            <button
              type="submit"
              disabled={isResearching || !query.trim()}
              className="absolute right-3 top-1/2 -translate-y-1/2 p-2 rounded-lg bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed transition-colors"
            >
              {isResearching ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <Send className="h-5 w-5" />
              )}
            </button>
          </form>
        </div>

        {/* Agent Status Panel */}
        <div className="mb-8 bg-gray-900 border border-gray-800 rounded-lg p-6">
          <h2 className="text-lg font-semibold mb-4">Agent Status Panel</h2>
          <div className="space-y-3">
            {Object.entries(agents).map(([agent, status]) => (
              <div key={agent} className="flex items-center gap-3">
                {status === "completed" ? (
                  <CheckCircle2 className="h-5 w-5 text-green-500" />
                ) : status === "running" ? (
                  <Loader2 className="h-5 w-5 text-blue-500 animate-spin" />
                ) : (
                  <div className="h-5 w-5 rounded-full border-2 border-gray-700" />
                )}
                <span className="capitalize text-gray-300">
                  {agent} Agent
                </span>
              </div>
            ))}
          </div>
          <p className="text-sm text-gray-500 mt-4">
            This makes the system feel alive.
          </p>
        </div>

        {/* Live Logs */}
        {logs.length > 0 && (
          <div className="mb-8 bg-gray-900 border border-gray-800 rounded-lg p-6">
            <h2 className="text-lg font-semibold mb-4">Live Logs</h2>
            <div className="bg-black rounded-lg p-4 max-h-64 overflow-y-auto font-mono text-sm space-y-1">
              {logs.map((log, index) => (
                <div key={index} className="text-gray-400">
                  {log}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Final Report Viewer */}
        {finalReport && (
          <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
            <div className="flex items-center gap-2 mb-4">
              <FileText className="h-5 w-5 text-blue-500" />
              <h2 className="text-lg font-semibold">Final Report</h2>
            </div>
            <div className="bg-black rounded-lg p-6 prose prose-invert max-w-none">
              <ReactMarkdown>{finalReport}</ReactMarkdown>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
