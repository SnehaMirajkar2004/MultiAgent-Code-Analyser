import time
from concurrent.futures import ThreadPoolExecutor

from app.agents.code_review_agent import CodeReviewAgent
from app.agents.bug_detection_agent import BugDetectionAgent
from app.agents.complexity_agent import ComplexityAgent
from app.agents.performance_agent import PerformanceAgent
from app.agents.validation_agent import run_validation_agent

review_agent = CodeReviewAgent()
bug_agent = BugDetectionAgent()
complexity_agent = ComplexityAgent()
performance_agent = PerformanceAgent()


def _safe_result(future, agent_name: str) -> dict:
    try:
        return future.result()
    except Exception as e:
        return {
            "error": True,
            "message": f"{agent_name} unexpected failure: {str(e)}"
        }


def analyze_code(code: str) -> dict:
    """
    Runs the four specialized agents in parallel, then runs the Validation
    Agent on their combined output. Returns a single structured report,
    plus timing info (useful for your Response Time evaluation metric).
    """
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=4) as executor:
        review_future = executor.submit(review_agent.run, code)
        time.sleep(0.3)
        bug_future = executor.submit(bug_agent.run, code)
        time.sleep(0.3)
        complexity_future = executor.submit(complexity_agent.run, code)
        time.sleep(0.3)
        performance_future = executor.submit(performance_agent.run, code)


        review_result = _safe_result(review_future, review_agent.name)
        bug_result = _safe_result(bug_future, bug_agent.name)
        complexity_result = _safe_result(complexity_future, complexity_agent.name)
        performance_result = _safe_result(performance_future, performance_agent.name)

    analysis_time = time.time() - start_time

    validation_result = run_validation_agent(
        code, review_result, bug_result, complexity_result, performance_result
    )

    total_time = time.time() - start_time

    return {
        "code_review": review_result,
        "bug_detection": bug_result,
        "complexity_analysis": complexity_result,
        "performance_optimization": performance_result,
        "validation": validation_result,
        "timing": {
            "analysis_time_seconds": round(analysis_time, 2),
            "total_time_seconds": round(total_time, 2),
        },
    }
