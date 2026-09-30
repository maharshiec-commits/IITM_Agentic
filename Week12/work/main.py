"""
================================================================================
BANKING MULTI-AGENT SYSTEM — MAIN ENTRY POINT
================================================================================
Week 12: Graded Mini Project
Use Case 1: Banking & Financial Services – Intelligent Customer Resolution

This is the main orchestrator that:
  1. Loads configuration and LLM settings
  2. Creates the 4 collaborating agents
  3. Runs customer queries through the sequential pipeline
  4. Displays results with clear handoff visibility

Architecture: Sequential Goal-Oriented Multi-Agent Flow
  Intent Classification → Policy Reasoning → Response Drafting → Risk & Escalation
================================================================================
"""

import os
import sys
import json
import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from crewai import Crew, Process

from agents import create_all_agents
from tasks import create_all_tasks
from config.mock_data import SAMPLE_QUERIES, get_customer_context


# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────
def setup_environment():
    """Load environment variables and configure the LLM."""
    # Load .env from project directory
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)
    
    # Check for API key
    google_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    openai_base = os.environ.get("OPENAI_API_BASE")
    model_env = os.environ.get("MODEL")
    
    if google_key:
        os.environ["GOOGLE_API_KEY"] = google_key
        llm_model = "gemini/gemini-2.0-flash"
        print(f"[CONFIG] Using Google Gemini (gemini-2.0-flash)")
    elif openai_key:
        # Use MODEL from .env if specified, otherwise default to gpt-4o-mini
        llm_model = model_env if model_env else "gpt-4o-mini"
        
        # Support custom API base (e.g., Vocareum proxy)
        if openai_base:
            os.environ["OPENAI_API_BASE"] = openai_base
            print(f"[CONFIG] Using OpenAI ({llm_model}) via custom endpoint: {openai_base}")
        else:
            print(f"[CONFIG] Using OpenAI ({llm_model})")
    else:
        print("=" * 60)
        print("ERROR: No LLM API key found!")
        print()
        print("Please set ONE of the following in your .env file:")
        print("  GOOGLE_API_KEY=your-gemini-api-key")
        print("  OPENAI_API_KEY=your-openai-api-key")
        print()
        print("Or set it as an environment variable before running:")
        print("  set GOOGLE_API_KEY=your-key-here")
        print("=" * 60)
        sys.exit(1)
    
    return llm_model


# ──────────────────────────────────────────────────────────────────────────────
# WORKFLOW EXECUTOR
# ──────────────────────────────────────────────────────────────────────────────
def run_single_query(query_data: dict, agents: dict, verbose: bool = True) -> dict:
    """
    Runs a single customer query through the full 4-agent pipeline.
    
    Args:
        query_data: Dict with 'customer_id' and 'query' keys
        agents: Dict of all 4 agents
        verbose: Whether to print detailed output
    
    Returns:
        Dict with results from each agent and final escalation decision
    """
    customer_id = query_data["customer_id"]
    customer_query = query_data["query"]
    query_id = query_data.get("id", "Q?")
    
    print("\n" + "=" * 80)
    print(f"  PROCESSING QUERY: {query_id}")
    print(f"  Customer: {customer_id}")
    print(f"  Query: {customer_query[:80]}...")
    print("=" * 80)
    
    # Create the sequential task pipeline with handoffs
    tasks = create_all_tasks(agents, customer_query, customer_id)
    
    # Create and run the Crew (sequential process = enforced handoffs)
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,  # Enforces Agent 1 → 2 → 3 → 4 order
        verbose=verbose,
    )
    
    # Execute the pipeline
    result = crew.kickoff()
    
    # Collect individual task outputs
    task_outputs = {}
    task_names = [
        "intent_classification",
        "policy_reasoning", 
        "response_drafting",
        "risk_escalation"
    ]
    for i, task in enumerate(tasks):
        task_outputs[task_names[i]] = str(task.output) if task.output else "No output"
    
    return {
        "query_id": query_id,
        "customer_id": customer_id,
        "query": customer_query,
        "final_output": str(result),
        "task_outputs": task_outputs,
    }


def print_result_summary(result: dict):
    """Prints a formatted summary of the query resolution."""
    print("\n" + "━" * 80)
    print(f"  RESOLUTION SUMMARY — {result['query_id']}")
    print("━" * 80)
    
    print(f"\n📋 Customer: {result['customer_id']}")
    print(f"📝 Query: {result['query'][:100]}...")
    
    print("\n" + "─" * 40)
    print("AGENT 1 — Intent Classification:")
    print("─" * 40)
    print(result["task_outputs"].get("intent_classification", "N/A")[:500])
    
    print("\n" + "─" * 40)
    print("AGENT 2 — Policy Reasoning:")
    print("─" * 40)
    print(result["task_outputs"].get("policy_reasoning", "N/A")[:500])
    
    print("\n" + "─" * 40)
    print("AGENT 3 — Response Drafting:")
    print("─" * 40)
    print(result["task_outputs"].get("response_drafting", "N/A")[:500])
    
    print("\n" + "─" * 40)
    print("AGENT 4 — Risk & Escalation Decision:")
    print("─" * 40)
    print(result["task_outputs"].get("risk_escalation", "N/A")[:500])
    
    print("\n" + "━" * 80)
    print("  FINAL OUTPUT")
    print("━" * 80)
    print(result["final_output"][:800])
    print("━" * 80 + "\n")


# ──────────────────────────────────────────────────────────────────────────────
# MAIN EXECUTION
# ──────────────────────────────────────────────────────────────────────────────
def main():
    """Main entry point: runs selected sample queries through the multi-agent pipeline."""
    
    print("=" * 80)
    print("  BANKING MULTI-AGENT SYSTEM — Intelligent Customer Resolution")
    print("  Week 12 Graded Mini Project | CrewAI Sequential Workflow")
    print("=" * 80)
    
    # Step 1: Setup
    llm_model = setup_environment()
    
    # Step 2: Create all agents
    print("\n[INIT] Creating 4 collaborating agents...")
    agents = create_all_agents(llm=llm_model)
    print("[INIT] Agents created:")
    for name, agent in agents.items():
        print(f"  → {name}: {agent.role}")
    
    # Step 3: Select queries to run
    # Choose a diverse subset that demonstrates all scenarios:
    #   Q1 = Duplicate charge (routine, LOW)
    #   Q3 = Fraud with large amount (CRITICAL escalation)
    #   Q4 = EMI bounce (MEDIUM)
    #   Q5 = Card block (routine, LOW)
    #   Q6 = Phishing victim (CRITICAL escalation)
    
    selected_query_ids = ["Q1", "Q3", "Q4", "Q5", "Q6"]
    
    # Allow command-line override
    if len(sys.argv) > 1:
        selected_query_ids = sys.argv[1:]
        print(f"\n[CONFIG] Running queries from command line: {selected_query_ids}")
    
    selected_queries = [q for q in SAMPLE_QUERIES if q["id"] in selected_query_ids]
    
    if not selected_queries:
        print(f"\n[ERROR] No matching queries found for IDs: {selected_query_ids}")
        print(f"Available IDs: {[q['id'] for q in SAMPLE_QUERIES]}")
        sys.exit(1)
    
    print(f"\n[CONFIG] Will process {len(selected_queries)} queries: "
          f"{[q['id'] for q in selected_queries]}")
    
    # Step 4: Run each query through the pipeline
    all_results = []
    
    for query_data in selected_queries:
        try:
            result = run_single_query(query_data, agents, verbose=True)
            all_results.append(result)
            print_result_summary(result)
        except Exception as e:
            print(f"\n[ERROR] Failed to process {query_data['id']}: {str(e)}")
            import traceback
            traceback.print_exc()
            all_results.append({
                "query_id": query_data["id"],
                "customer_id": query_data["customer_id"],
                "query": query_data["query"],
                "final_output": f"ERROR: {str(e)}",
                "task_outputs": {},
            })
    
    # Step 5: Save results
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = Path(__file__).parent / f"output_results_{timestamp}.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[DONE] Results saved to: {output_file}")
    
    # Step 6: Print final summary table
    print("\n" + "=" * 80)
    print("  EXECUTION SUMMARY")
    print("=" * 80)
    print(f"{'Query':<8} {'Customer':<12} {'Status':<12} {'Description':<48}")
    print("─" * 80)
    for r in all_results:
        status = "ERROR" if r["final_output"].startswith("ERROR") else "COMPLETED"
        print(f"{r['query_id']:<8} {r['customer_id']:<12} {status:<12} {r['query'][:48]}")
    print("=" * 80)


if __name__ == "__main__":
    main()
