"""End-to-end verification of full autonomous agent mission and report generation."""
import sys
import os
import time
import json
import queue
import threading
import datetime
import urllib.parse

# Ensure utf-8 stdout encoding on Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from autonomous_agent_app import AutonomousAgent

def test_full_mission():
    q = queue.Queue()
    agent = AutonomousAgent(q)
    
    print("Launching test mission: 'Solid-State Battery Breakthroughs' (Quick)...")
    agent.start_mission("Solid-State Battery Breakthroughs", depth_mode="Quick (3 Steps)")
    
    start = time.time()
    last_report = ""
    completed = False
    
    while time.time() - start < 30:
        while not q.empty():
            msg = q.get_nowait()
            mtype = msg.get("type")
            data = msg.get("data")
            if mtype == "LOG":
                print(f"  [{data['level']}] {data['text'][:80]}...")
            elif mtype == "STATUS" and data == "COMPLETED":
                completed = True
            elif mtype == "REPORT_UPDATED":
                last_report = data.get("report", "")
        if completed:
            break
        time.sleep(0.5)

    assert completed, "Mission should have completed"
    assert "AUTONOMOUS INTELLIGENCE REPORT" in last_report, "Report should contain title"
    assert len(last_report) > 300, "Report should contain substantial content"
    print("\n--- GENERATED REPORT SNIPPET ---")
    print(last_report[:400])
    print("--------------------------------")
    print("FULL MISSION TEST PASSED! [OK]")

if __name__ == "__main__":
    test_full_mission()
