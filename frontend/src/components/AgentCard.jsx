import React from "react";

const ACCENTS = {
  review: { text: "text-review", bg: "bg-review", border: "border-review" },
  bug: { text: "text-bug", bg: "bg-bug", border: "border-bug" },
  complexity: { text: "text-complexity", bg: "bg-complexity", border: "border-complexity" },
  performance: { text: "text-performance", bg: "bg-performance", border: "border-performance" },
  validation: { text: "text-validation", bg: "bg-validation", border: "border-validation" },
};

export function SeverityBadge({ severity }) {
  const colors = {
    High: "bg-bug/15 text-bug border-bug/40",
    Medium: "bg-complexity/15 text-complexity border-complexity/40",
    Low: "bg-console-600/30 text-console-200 border-console-600",
  };
  return (
    <span
      className={`text-[11px] font-mono px-2 py-0.5 rounded border ${
        colors[severity] || colors.Low
      }`}
    >
      {severity || "Low"}
    </span>
  );
}

export function VerdictBadge({ verdict }) {
  const colors = {
    Confirmed: "bg-performance/15 text-performance border-performance/40",
    Likely: "bg-complexity/15 text-complexity border-complexity/40",
    Unsupported: "bg-bug/15 text-bug border-bug/40",
  };
  return (
    <span
      className={`text-[11px] font-mono px-2 py-0.5 rounded border ${
        colors[verdict] || "bg-console-600/30 text-console-200 border-console-600"
      }`}
    >
      {verdict || "Unverified"}
    </span>
  );
}

export default function AgentCard({ accent, agentNumber, title, subtitle, children }) {
  const c = ACCENTS[accent] || ACCENTS.review;

  return (
    <div className="bg-console-900 border border-console-700 rounded-xl overflow-hidden">
      <div className={`flex items-center gap-3 px-5 py-3 border-b border-console-700`}>
        <span
          className={`w-6 h-6 flex items-center justify-center rounded-full text-[11px] font-mono font-bold text-console-950 ${c.bg}`}
        >
          {agentNumber}
        </span>
        <div>
          <h3 className={`font-mono text-sm font-semibold ${c.text}`}>{title}</h3>
          {subtitle && <p className="text-xs text-console-400">{subtitle}</p>}
        </div>
      </div>
      <div className="p-5">{children}</div>
    </div>
  );
}
