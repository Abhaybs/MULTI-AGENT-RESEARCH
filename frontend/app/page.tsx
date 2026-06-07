"use client";

import { useState, useEffect, useRef } from "react";
import { Send, CheckCircle2, Loader2, FileText, Sparkles, Brain, Search, BookOpen, Filter, Shield, PenTool, Quote, Clock } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { motion, AnimatePresence } from "framer-motion";

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

interface LogEntry {
  message: string;
  timestamp: string;
  level: string; // info, success, warning, error
}

const agentIcons: Record<keyof AgentState, any> = {
  planner: Brain,
  researcher: Search,
  paper_analyzer: BookOpen,
  insight_extractor: Sparkles,
  source_ranker: Filter,
  critic: Shield,
  writer: PenTool,
  citation_agent: Quote,
};

const agentLabels: Record<keyof AgentState, string> = {
  planner: "Planner",
  researcher: "Researcher",
  paper_analyzer: "Paper Analyzer",
  insight_extractor: "Insight Extractor",
  source_ranker: "Source Ranker",
  critic: "Critic",
  writer: "Writer",
  citation_agent: "Citation Agent",
};

// Color coding for log levels
const logColors: Record<string, string> = {
  info: "text-blue-300 border-blue-500/30",
  success: "text-green-300 border-green-500/30",
  warning: "text-yellow-300 border-yellow-500/30",
  error: "text-red-300 border-red-500/30",
};

export default function Home() {
  const [query, setQuery] = useState("");
  const [logs, setLogs] = useState<LogEntry[]>([]);
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
  
  // Ref for auto-scrolling logs
  const logsEndRef = useRef<HTMLDivElement>(null);
  
  // Auto-scroll to bottom when new logs arrive
  useEffect(() => {
    if (logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [logs]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsResearching(true);
    setLogs([]);
    setFinalReport("");
    setAgents({
      planner: "idle",
      researcher: "idle",
      paper_analyzer: "idle",
      insight_extractor: "idle",
      source_ranker: "idle",
      critic: "idle",
      writer: "idle",
      citation_agent: "idle",
    });

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

          buffer = lines.pop() || "";

          for (const line of lines) {
            if (line.startsWith("data: ")) {
              try {
                const jsonStr = line.slice(6).trim();
                if (jsonStr) {
                  const data = JSON.parse(jsonStr);

                  if (data.type === "agent_status") {
                    setAgents((prev) => ({
                      ...prev,
                      [data.agent]: data.status,
                    }));
                  } else if (data.type === "log") {
                    setLogs((prev) => [...prev, {
                      message: data.message,
                      timestamp: data.timestamp,
                      level: data.level || "info"
                    }]);
                  } else if (data.type === "final_report") {
                    setFinalReport(data.report);
                  }
                }
              } catch (e) {
                console.error("Error parsing SSE message:", e);
              }
            }
          }
        }
      }
    } catch (error) {
      console.error("Error:", error);
      setLogs((prev) => [...prev, {
        message: "❌ Error connecting to backend",
        timestamp: new Date().toLocaleTimeString(),
        level: "error"
      }]);
    } finally {
      setIsResearching(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-black text-gray-100">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-r from-blue-500/5 to-purple-500/5 blur-3xl animate-pulse" />
        <div className="absolute -bottom-1/2 -right-1/2 w-full h-full bg-gradient-to-l from-cyan-500/5 to-pink-500/5 blur-3xl animate-pulse delay-1000" />
      </div>

      <div className="relative container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-12 text-center"
        >
          <h1 className="text-6xl font-black mb-3 bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent animate-gradient">
            AI Research Assistant
          </h1>
          <p className="text-gray-400 text-lg font-light tracking-wide">
            Powered by LangGraph • 8-Agent Multi-Source Research System
          </p>
        </motion.header>

        {/* Search Input */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mb-10"
        >
          <form onSubmit={handleSubmit} className="relative group">
            <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-2xl opacity-30 group-hover:opacity-50 blur transition duration-500" />
            <div className="relative">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter your research topic... (e.g., Quantum Computing)"
                className="w-full bg-gray-900/90 backdrop-blur-xl border border-gray-800/50 rounded-2xl px-8 py-5 pr-16 text-gray-100 placeholder-gray-500 focus:outline-none focus:border-purple-500/50 focus:ring-2 focus:ring-purple-500/20 transition-all duration-300 text-lg"
                disabled={isResearching}
              />
              <button
                type="submit"
                disabled={isResearching || !query.trim()}
                className="absolute right-3 top-1/2 -translate-y-1/2 p-3 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 disabled:from-gray-700 disabled:to-gray-800 disabled:cursor-not-allowed transition-all duration-300 shadow-lg hover:shadow-purple-500/50 hover:scale-105 active:scale-95"
              >
                {isResearching ? (
                  <Loader2 className="h-6 w-6 animate-spin" />
                ) : (
                  <Send className="h-6 w-6" />
                )}
              </button>
            </div>
          </form>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Agent Status Panel - Sticky */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="lg:col-span-1"
          >
            <div className="sticky top-8 bg-gray-900/50 backdrop-blur-xl border border-gray-800/50 rounded-2xl p-6 shadow-2xl">
              <h2 className="text-xl font-bold mb-6 flex items-center gap-3">
                <Sparkles className="h-5 w-5 text-purple-400" />
                Agent Pipeline
              </h2>
              <div className="space-y-3">
                {Object.entries(agents).map(([agent, status], index) => {
                  const Icon = agentIcons[agent as keyof AgentState];
                  return (
                    <motion.div
                      key={agent}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.05 }}
                      className={`flex items-center gap-4 p-3 rounded-xl transition-all duration-300 ${
                        status === "running"
                          ? "bg-blue-500/10 border border-blue-500/30 shadow-lg shadow-blue-500/10"
                          : status === "completed"
                          ? "bg-green-500/10 border border-green-500/30"
                          : "bg-gray-800/30 border border-gray-700/30"
                      }`}
                    >
                      <div className="relative">
                        {status === "completed" ? (
                          <motion.div
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            transition={{ type: "spring", stiffness: 200, damping: 10 }}
                          >
                            <CheckCircle2 className="h-6 w-6 text-green-400" />
                          </motion.div>
                        ) : status === "running" ? (
                          <Loader2 className="h-6 w-6 text-blue-400 animate-spin" />
                        ) : (
                          <Icon className="h-6 w-6 text-gray-600" />
                        )}
                      </div>
                      <div className="flex-1">
                        <span className="text-sm font-medium text-gray-300">
                          {agentLabels[agent as keyof AgentState]}
                        </span>
                      </div>
                      {status === "running" && (
                        <motion.div
                          animate={{ opacity: [0.4, 1, 0.4] }}
                          transition={{ duration: 1.5, repeat: Infinity }}
                          className="w-2 h-2 rounded-full bg-blue-400"
                        />
                      )}
                    </motion.div>
                  );
                })}
              </div>
              <p className="text-xs text-gray-500 mt-6 text-center italic">
                Watch the AI agents collaborate in real-time
              </p>
            </div>
          </motion.div>

          {/* Main Content Area */}
          <div className="lg:col-span-2 space-y-6">
            {/* Live Logs */}
            <AnimatePresence>
              {logs.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.4 }}
                  className="bg-gray-900/50 backdrop-blur-xl border border-gray-800/50 rounded-2xl p-6 shadow-2xl"
                >
                  <h2 className="text-xl font-bold mb-4 flex items-center gap-3">
                    {isResearching ? (
                      <Loader2 className="h-5 w-5 text-blue-400 animate-spin" />
                    ) : (
                      <Clock className="h-5 w-5 text-green-400" />
                    )}
                    Live Activity Logs
                  </h2>
                  <div className="bg-black/40 rounded-xl p-5 max-h-96 overflow-y-auto font-mono text-sm space-y-2 scrollbar-thin scrollbar-thumb-gray-700 scrollbar-track-gray-900">
                    <AnimatePresence mode="popLayout">
                      {logs.map((log, index) => (
                        <motion.div
                          key={index}
                          initial={{ opacity: 0, x: -10, height: 0 }}
                          animate={{ opacity: 1, x: 0, height: "auto" }}
                          exit={{ opacity: 0, x: 10, height: 0 }}
                          transition={{ 
                            duration: 0.3,
                            delay: index * 0.02 
                          }}
                          className={`${logColors[log.level] || logColors.info} hover:bg-gray-800/30 transition-colors py-2 px-3 rounded-lg border-l-2 flex items-start gap-3`}
                        >
                          <span className="text-gray-500 text-xs font-semibold min-w-[60px] mt-0.5">
                            [{log.timestamp}]
                          </span>
                          <motion.span
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ duration: 0.5, delay: 0.1 }}
                            className="flex-1"
                          >
                            {log.message}
                          </motion.span>
                        </motion.div>
                      ))}
                    </AnimatePresence>
                    {/* Invisible div for auto-scroll */}
                    <div ref={logsEndRef} />
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Final Report */}
            <AnimatePresence>
              {finalReport && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.5 }}
                  className="bg-gray-900/50 backdrop-blur-xl border border-gray-800/50 rounded-2xl p-8 shadow-2xl"
                >
                  <div className="flex items-center gap-3 mb-6">
                    <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg">
                      <FileText className="h-6 w-6" />
                    </div>
                    <h2 className="text-2xl font-bold">Research Report</h2>
                  </div>
                  <div className="bg-black/20 rounded-xl p-8 prose prose-invert prose-lg max-w-none prose-headings:font-bold prose-h1:text-4xl prose-h1:mb-6 prose-h1:bg-gradient-to-r prose-h1:from-blue-400 prose-h1:to-purple-400 prose-h1:bg-clip-text prose-h1:text-transparent prose-h2:text-2xl prose-h2:mt-8 prose-h2:mb-4 prose-h2:text-gray-200 prose-p:text-gray-300 prose-p:leading-relaxed prose-a:text-blue-400 prose-a:no-underline hover:prose-a:text-blue-300 prose-strong:text-gray-200 prose-ul:text-gray-300 prose-ol:text-gray-300 prose-code:text-pink-400 prose-code:bg-gray-800 prose-code:px-2 prose-code:py-1 prose-code:rounded">
                    <ReactMarkdown>{finalReport}</ReactMarkdown>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
}
