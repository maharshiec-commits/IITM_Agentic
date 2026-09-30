"""Test script to verify AutonomousAgent engine, tool execution, and stop handling headlessly."""
import queue
import time
from autonomous_agent_app import AutonomousAgent, AgentTools

def test_tools():
    print("Testing Wikipedia search tool...")
    results = AgentTools.search_wikipedia("Artificial Intelligence", max_results=2)
    print(f"  -> Search returned {len(results)} items: {[r['title'] for r in results]}")
    assert len(results) > 0, "Tool should return at least 1 result"
    
    print("Testing Wikipedia details fetch...")
    details = AgentTools.fetch_wikipedia_details(results[0]['title'])
    print(f"  -> Details length: {len(details)} chars")
    assert len(details) > 0, "Details should not be empty"

    print("Testing insight extraction...")
    insights = AgentTools.extract_insights(details, "Artificial Intelligence")
    print(f"  -> Extracted {len(insights)} insights: {insights[:1]}")
    print("Tools test PASSED! \n")

def test_agent_stop_functionality():
    print("Testing Agent Stop Signal responsiveness...")
    q = queue.Queue()
    agent = AutonomousAgent(q)
    
    agent.start_mission("Quantum Computing", depth_mode="Quick (3 Steps)")
    time.sleep(1.5) # Let it start
    
    print("Issuing STOP command...")
    agent.stop()
    time.sleep(1.0)
    
    # Collect queue events
    events = []
    while not q.empty():
        events.append(q.get_nowait())
    
    status_events = [e for e in events if e.get("type") == "STATUS"]
    print(f"  -> Status events emitted: {[e.get('data') for e in status_events]}")
    assert any(e.get("data") == "STOPPED" or e.get("data") == "STOPPING" for e in status_events), "Agent must emit STOPPED status"
    assert not agent.is_running, "Agent must not be running after stop"
    print("Stop test PASSED! \n")

if __name__ == "__main__":
    test_tools()
    test_agent_stop_functionality()
    print("ALL TESTS PASSED SUCCESSFULLY! [OK]")
