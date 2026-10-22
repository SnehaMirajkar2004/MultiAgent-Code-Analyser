import React from "react";
import AgentCard, { SeverityBadge, VerdictBadge } from "./AgentCard.jsx";

function AgentError({ message }) {
  return (
    <p className="text-sm text-bug font-mono">
      ⚠ {message || "This agent failed to return a result. Try again."}
    </p>
  );
}

function EmptyNote({ text }) {
  return <p className="text-sm text-console-400 italic">{text}</p>;
}

export default function ReportView({ report }) {
  const { code_review, bug_detection, complexity_analysis, performance_optimization, validation, timing } =
    report;

  const confidenceColor =
    {
      High: "text-performance",
      Medium: "text-complexity",
      Low: "text-bug",
    }[validation?.overall_confidence] || "text-console-200";

  return (
    <div className="space-y-6">
      {/* Top summary bar */}
      <div className="bg-console-900 border border-console-700 rounded-xl p-5 flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-xs text-console-400 font-mono uppercase tracking-wide">
            Overall confidence
          </p>
          <p className={`text-lg font-mono font-bold ${confidenceColor}`}>
            {validation?.overall_confidence || "N/A"}
          </p>
        </div>
        <div>
          <p className="text-xs text-console-400 font-mono uppercase tracking-wide">
            Agent analysis time
          </p>
          <p className="text-lg font-mono font-bold text-console-200">
            {timing?.analysis_time_seconds ?? "-"}s
          </p>
        </div>
        <div>
          <p className="text-xs text-console-400 font-mono uppercase tracking-wide">
            Total (incl. validation)
          </p>
          <p className="text-lg font-mono font-bold text-console-200">
            {timing?.total_time_seconds ?? "-"}s
          </p>
        </div>
        <div>
          <p className="text-xs text-console-400 font-mono uppercase tracking-wide">
            PostgreSQL Storage
          </p>
          {report.db_record?.saved ? (
            <p className="text-sm font-mono font-bold text-performance">
              ✓ Saved #{report.db_record.id}
            </p>
          ) : (
            <p className="text-xs font-mono text-console-400">
              Bypassed
            </p>
          )}
        </div>
      </div>

      {/* 1. Code Review */}
      <AgentCard accent="review" agentNumber="1" title="Code Review Agent" subtitle="Quality, readability, best practices">
        {code_review?.error ? (
          <AgentError message={code_review.message} />
        ) : (
          <>
            {Array.isArray(code_review?.issues) && code_review.issues.length > 0 ? (
              <ul className="space-y-3 mb-3">
                {code_review.issues.map((issue, i) => (
                  <li key={i} className="border-l-2 border-review/40 pl-3">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-sm font-medium text-console-200">{issue.title}</span>
                      <SeverityBadge severity={issue.severity} />
                    </div>
                    <p className="text-sm text-console-400">{issue.description}</p>
                    {issue.suggestion && (
                      <p className="text-sm text-review/90 mt-1">→ {issue.suggestion}</p>
                    )}
                  </li>
                ))}
              </ul>
            ) : (
              <EmptyNote text="No readability or best-practice issues found." />
            )}
            {code_review?.summary && (
              <p className="text-sm text-console-400 border-t border-console-700 pt-3 mt-3">
                {code_review.summary}
              </p>
            )}
          </>
        )}
      </AgentCard>

      {/* 2. Bug Detection */}
      <AgentCard accent="bug" agentNumber="2" title="Bug Detection Agent" subtitle="Syntax, logical, and runtime issues">
        {bug_detection?.error ? (
          <AgentError message={bug_detection.message} />
        ) : (
          <>
            {Array.isArray(bug_detection?.bugs) && bug_detection.bugs.length > 0 ? (
              <ul className="space-y-3 mb-3">
                {bug_detection.bugs.map((bug, i) => (
                  <li key={i} className="border-l-2 border-bug/40 pl-3">
                    <div className="flex items-center gap-2 mb-1 flex-wrap">
                      <span className="text-sm font-medium text-console-200 uppercase font-mono text-xs">
                        {bug.type}
                      </span>
                      <SeverityBadge severity={bug.severity} />
                    </div>
                    <p className="text-sm text-console-400">{bug.description}</p>
                    {bug.location_hint && (
                      <p className="text-xs text-console-600 font-mono mt-1">{bug.location_hint}</p>
                    )}
                  </li>
                ))}
              </ul>
            ) : (
              <EmptyNote text="No bugs detected." />
            )}
            {bug_detection?.summary && (
              <p className="text-sm text-console-400 border-t border-console-700 pt-3 mt-3">
                {bug_detection.summary}
              </p>
            )}
          </>
        )}
      </AgentCard>

      {/* 3. Complexity */}
      <AgentCard accent="complexity" agentNumber="3" title="Complexity Analysis Agent" subtitle="Time and space complexity">
        {complexity_analysis?.error ? (
          <AgentError message={complexity_analysis.message} />
        ) : (
          <>
            <div className="flex gap-6 mb-3">
              <div>
                <p className="text-xs text-console-400 font-mono uppercase">Time</p>
                <p className="text-xl font-mono font-bold text-complexity">
                  {complexity_analysis?.time_complexity || "N/A"}
                </p>
              </div>
              <div>
                <p className="text-xs text-console-400 font-mono uppercase">Space</p>
                <p className="text-xl font-mono font-bold text-complexity">
                  {complexity_analysis?.space_complexity || "N/A"}
                </p>
              </div>
            </div>
            {complexity_analysis?.explanation && (
              <p className="text-sm text-console-400">{complexity_analysis.explanation}</p>
            )}
          </>
        )}
      </AgentCard>

      {/* 4. Performance */}
      <AgentCard accent="performance" agentNumber="4" title="Performance Optimization Agent" subtitle="Selective, justified efficiency improvements">
        {performance_optimization?.error ? (
          <AgentError message={performance_optimization.message} />
        ) : (
          <>
            {Array.isArray(performance_optimization?.suggestions) && performance_optimization.suggestions.length > 0 ? (
              <ul className="space-y-3 mb-3">
                {performance_optimization.suggestions.map((s, i) => (
                  <li key={i} className="border-l-2 border-performance/40 pl-3">
                    <p className="text-sm text-console-200">{s.issue}</p>
                    <p className="text-sm text-performance/90 mt-1">→ {s.suggestion}</p>
                    {s.expected_improvement && (
                      <p className="text-xs text-console-600 font-mono mt-1">
                        {s.expected_improvement}
                      </p>
                    )}
                  </li>
                ))}
              </ul>
            ) : (
              <EmptyNote
                text={
                  performance_optimization?.is_already_efficient
                    ? "Code is already efficient — no changes suggested."
                    : "No optimization suggestions."
                }
              />
            )}
            {performance_optimization?.summary && (
              <p className="text-sm text-console-400 border-t border-console-700 pt-3 mt-3">
                {performance_optimization.summary}
              </p>
            )}
          </>
        )}
      </AgentCard>

      {/* 5. Validation */}
      <AgentCard accent="validation" agentNumber="5" title="Validation Agent" subtitle="Cross-checks findings from all other agents">
        {validation?.error ? (
          <AgentError message={validation.message} />
        ) : (
          <>
            {Array.isArray(validation?.bug_validations) && validation.bug_validations.length > 0 && (
              <div className="mb-4">
                <p className="text-xs text-console-400 font-mono uppercase mb-2">Bug findings</p>
                <ul className="space-y-2">
                  {validation.bug_validations.map((v, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <VerdictBadge verdict={v.verdict} />
                      <span className="text-sm text-console-400">
                        {v.description} — <span className="text-console-200">{v.note}</span>
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {Array.isArray(validation?.optimization_validations) && validation.optimization_validations.length > 0 && (
              <div className="mb-4">
                <p className="text-xs text-console-400 font-mono uppercase mb-2">
                  Optimization suggestions
                </p>
                <ul className="space-y-2">
                  {validation.optimization_validations.map((v, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <VerdictBadge verdict={v.verdict} />
                      <span className="text-sm text-console-400">
                        {v.description} — <span className="text-console-200">{v.note}</span>
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {validation?.consistency_notes && (
              <p className="text-sm text-console-400 mb-3">
                <span className="text-console-200 font-medium">Consistency: </span>
                {validation.consistency_notes}
              </p>
            )}
            {validation?.validated_summary && (
              <p className="text-sm text-console-200 border-t border-console-700 pt-3 mt-3">
                {validation.validated_summary}
              </p>
            )}
          </>
        )}
      </AgentCard>
    </div>
  );
}
