"""
Quick single-query runner for testing / demonstration.
Usage:
  python run_single_query.py                  # Runs default query Q1
  python run_single_query.py Q3               # Runs specific query by ID
  python run_single_query.py --custom          # Enter your own query interactively
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from crewai import Crew, Process

from agents import create_all_agents
from tasks import create_all_tasks
from config.mock_data import SAMPLE_QUERIES, CUSTOMER_DATABASE


def setup():
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)
    
    google_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    openai_base = os.environ.get("OPENAI_API_BASE")
    model_env = os.environ.get("MODEL")
    
    if google_key:
        os.environ["GOOGLE_API_KEY"] = google_key
        return "gemini/gemini-2.0-flash"
    elif openai_key:
        llm_model = model_env if model_env else "gpt-4o-mini"
        if openai_base:
            os.environ["OPENAI_API_BASE"] = openai_base
            print(f"[CONFIG] Using {llm_model} via {openai_base}")
        return llm_model
    else:
        print("ERROR: No API key found. Set GOOGLE_API_KEY or OPENAI_API_KEY in .env")
        sys.exit(1)


def main():
    llm_model = setup()
    agents = create_all_agents(llm=llm_model)
    
    # Determine which query to run
    if len(sys.argv) > 1 and sys.argv[1] == "--custom":
        print("\nAvailable customers:")
        for cid, cdata in CUSTOMER_DATABASE.items():
            print(f"  {cid}: {cdata['name']}")
        customer_id = input("\nEnter Customer ID (e.g., CUST001): ").strip() or "CUST001"
        query_text = input("Enter your query: ").strip()
        if not query_text:
            print("No query entered. Exiting.")
            sys.exit(1)
        query_data = {
            "id": "CUSTOM",
            "customer_id": customer_id,
            "query": query_text
        }
    else:
        query_id = sys.argv[1] if len(sys.argv) > 1 else "Q1"
        query_data = next((q for q in SAMPLE_QUERIES if q["id"] == query_id), None)
        if not query_data:
            print(f"Query {query_id} not found. Available: {[q['id'] for q in SAMPLE_QUERIES]}")
            sys.exit(1)
    
    print(f"\n{'='*70}")
    print(f"  Running Query: {query_data['id']}")
    print(f"  Customer: {query_data['customer_id']}")
    print(f"  Query: {query_data['query'][:80]}...")
    print(f"{'='*70}\n")
    
    tasks = create_all_tasks(agents, query_data["query"], query_data["customer_id"])
    
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )
    
    result = crew.kickoff()
    
    print(f"\n{'='*70}")
    print("  FINAL RESULT")
    print(f"{'='*70}")
    print(result)
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
