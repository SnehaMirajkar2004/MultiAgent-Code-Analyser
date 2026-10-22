import React, { useRef, useState } from "react";

export default function CodeInput({ onAnalyze, isLoading }) {
  const [mode, setMode] = useState("paste"); // "paste" | "upload"
  const [code, setCode] = useState("");
  const [file, setFile] = useState(null);
  const fileInputRef = useRef(null);

  const canSubmit =
    !isLoading && ((mode === "paste" && code.trim()) || (mode === "upload" && file));

  const handleFileChange = (e) => {
    const f = e.target.files?.[0];
    if (f && f.name.endsWith(".py")) {
      setFile(f);
    } else if (f) {
      alert("Only .py files are supported.");
      e.target.value = "";
    }
  };

  const handleSubmit = () => {
    if (!canSubmit) return;
    onAnalyze({ mode, code, file });
  };

  return (
    <div className="bg-console-900 border border-console-700 rounded-xl overflow-hidden">
      {/* Tab bar */}
      <div className="flex items-center justify-between border-b border-console-700 px-4 pt-3">
        <div className="flex gap-1">
          {["paste", "upload"].map((m) => (
            <button
              key={m}
              onClick={() => setMode(m)}
              className={`px-4 py-2 text-sm font-mono rounded-t-lg transition-colors ${
                mode === m
                  ? "bg-console-950 text-review border-t border-x border-console-700"
                  : "text-console-400 hover:text-console-200"
              }`}
            >
              {m === "paste" ? "Paste code" : "Upload .py"}
            </button>
          ))}
        </div>
        <span className="text-xs text-console-400 font-mono pb-2 hidden sm:block">
          input.py
        </span>
      </div>

      <div className="p-4">
        {mode === "paste" ? (
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder={"def example(n):\n    total = 0\n    for i in range(n):\n        total += i\n    return total"}
            spellCheck={false}
            className="code-input w-full h-72 bg-console-950 text-console-200 border border-console-700 rounded-lg p-4 text-sm leading-relaxed resize-y focus:outline-none focus:border-review placeholder:text-console-600"
          />
        ) : (
          <div
            onClick={() => fileInputRef.current?.click()}
            className="h-72 flex flex-col items-center justify-center gap-3 border-2 border-dashed border-console-700 rounded-lg cursor-pointer hover:border-review transition-colors"
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".py"
              onChange={handleFileChange}
              className="hidden"
            />
            <div className="text-console-400 font-mono text-sm">
              {file ? (
                <span className="text-review">{file.name}</span>
              ) : (
                "Click to choose a .py file"
              )}
            </div>
            {file && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setFile(null);
                  if (fileInputRef.current) fileInputRef.current.value = "";
                }}
                className="text-xs text-console-400 underline hover:text-bug"
              >
                Remove
              </button>
            )}
          </div>
        )}

        <button
          onClick={handleSubmit}
          disabled={!canSubmit}
          className="mt-4 w-full py-3 rounded-lg font-mono text-sm font-medium transition-colors bg-review text-console-950 disabled:bg-console-700 disabled:text-console-400 disabled:cursor-not-allowed hover:brightness-110"
        >
          {isLoading ? "Running 5-agent analysis..." : "Analyze code"}
        </button>
      </div>
    </div>
  );
}
