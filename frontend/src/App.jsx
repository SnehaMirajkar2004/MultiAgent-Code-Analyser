import React, { useState } from "react";
import CodeInput from "./components/CodeInput.jsx";
import ReportView from "./components/ReportView.jsx";

const API_URL = "http://localhost:8000/api/analyze";

export default function App() {
  const [report, setReport] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async ({ mode, code, file }) => {
    setIsLoading(true);
    setError(null);
    setReport(null);

    try {
      const formData = new FormData();
      if (mode === "upload" && file) {
        formData.append("file", file);
      } else {
        formData.append("code", code);
      }

      const res = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const errBody = await res.json().catch(() => ({}));
        throw new Error(errBody.detail || `Request failed with status ${res.status}`);
      }

      const data = await res.json();
      setReport(data);
    } catch (err) {
      setError(
        err.message?.includes("Failed to fetch")
          ? "Could not reach the backend. Make sure the FastAPI server is running on http://localhost:8000."
          : err.message
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-console-950 text-console-200">
      {/* Header */}
      <header className="border-b border-console-700 px-6 py-5">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="font-mono text-lg font-bold text-console-200">
              Multi-Agent Code Analyzer
            </h1>
            <p className="text-xs text-console-400">
              Code Review · Bug Detection · Complexity · Performance · Validation
            </p>
          </div>
          <div className="hidden sm:flex items-center gap-2 text-xs font-mono text-console-400">
            <span className="w-2 h-2 rounded-full bg-performance pulse-dot" />
            5 agents ready
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-4xl mx-auto px-6 py-8 space-y-6">
        <CodeInput onAnalyze={handleAnalyze} isLoading={isLoading} />

        {error && (
          <div className="bg-bug/10 border border-bug/40 rounded-xl p-4">
            <p className="text-sm text-bug font-mono">⚠ {error}</p>
          </div>
        )}

        {isLoading && (
          <div className="bg-console-900 border border-console-700 rounded-xl p-8 text-center">
            <p className="text-sm text-console-400 font-mono">
              Running 4 agents in parallel, then validating results
              <span className="pulse-dot">...</span>
            </p>
          </div>
        )}

        {report && !isLoading && <ReportView report={report} />}
      </main>

      <footer className="max-w-4xl mx-auto px-6 py-8 text-xs text-console-600 font-mono">
        Prototype — SY MCA Research Project · Multi-Agent AI System for Code Analysis
      </footer>
    </div>
  );
}
