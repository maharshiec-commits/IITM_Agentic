# ApexBank AI Advisory & Support Copilot — Industry Capstone Project

**Course**: Professional Certificate Programme in Agentic AI  
**Capstone**: Design, Build, Evaluate an AI Agent (Week 21)  
**Scenario**: Scenario 2 — Banking: AI Banking Support & Advisory Agent (Non-Transactional)  
**Author / Consultant**: Maharshi (Applied AI Consultant & AI Engineer)  

---

## Executive Overview

This Capstone project delivers **ApexBank AI Advisory Copilot**, an enterprise-grade, non-transactional AI banking advisory system engineered for **Apex Global Bank**. Operating under strict financial safety mandates, the system handles customer inquiries regarding account balances, loan EMI calculations, fixed deposit rates, foreign exchange conversions, KYC regulatory procedures, and urgent fraud escalations.

Built following an industry-standard engineering progression across **Phases 1 through 9**, the agent demonstrates:
1. **Non-Transactional Safety**: Deterministic interception and refusal of fund transfers, password modifications, or financial guarantees.
2. **Deterministic Financial Tools**: Exact reducing-balance EMI math, read-only account balance lookups, live forex rates, and support ticket creation.
3. **Regulatory RAG Knowledge Base**: High-dimensional FAISS semantic search across 4 authoritative banking policy and fee schedule documents.
4. **Conversational Memory**: Sliding window buffer memory ($k=6$) with automatic pronoun resolution across multi-turn dialogues.
5. **Continuous Adaptive Learning**: Feedback engine storing user ratings and corrections to dynamically adjust future inference context.
6. **Zero-PII Telemetry**: Automated PII sanitizer masking card numbers, accounts, Aadhaar, and phone numbers in audit logs.
7. **Visual Pipeline Flow**: Full visual architecture exported in Langflow JSON format.

---

## Project Structure & Deliverables

```
Week21/work/
├── 1_PROBLEM_FRAMING.md             # Deliverable 1: Problem framing, personas, success criteria
├── 2_DEMO_SCRIPT_AND_LOGS.md        # Deliverable 2: 5 forced demo interactions + evidence logs
├── 3_PROMPT_COMPARISON.md           # Deliverable 3: 3 prompt variants benchmarked across same test set
├── 4_EVALUATION_REPORT.md           # Deliverable 4: Evaluation report, metrics, debugged failure case
├── 5_ENGINEERING_JUSTIFICATION.md   # Deliverable 5: Architectural tradeoffs, safety, deployment roadmap
├── README.md                        # This master guide & setup instructions
├── agent.py                         # Production cognitive orchestrator (Safety -> Plan -> RAG -> Tools -> Memory)
├── tools.py                         # Banking tools, Pydantic schemas, and safety guardrail
├── rag_engine.py                    # Semantic chunking, OpenAI embeddings, and FAISS vector index
├── memory_and_planner.py            # Sliding window memory and task decomposition planner
├── adaptive_engine.py               # Feedback collection & dynamic context adjustment engine
├── safe_logger.py                   # PII sanitization engine & latency telemetry logger
├── app.py                           # Interactive Streamlit visual application
├── main.py                          # Interactive CLI runner
├── phase2_baseline_agent.py         # Phase 2 baseline rule-based agent demonstration
├── phase3_prompt_evaluation.py      # Phase 3 automated prompt comparison benchmark
├── run_capstone_evaluation.py       # Phase 9 automated end-to-end evaluation harness
├── apex_bank_copilot_langflow.json  # Exported Langflow visual pipeline
├── data/                            # Regulatory banking policy documents
│   ├── banking_policies.txt
│   ├── kyc_and_compliance.txt
│   ├── loan_and_interest_terms.txt
│   └── fee_schedule.txt
├── logs/                            # PII-sanitized telemetry & evaluation logs
│   ├── telemetry_audit.log
│   └── evaluation_run_report.json
├── vectorstore/                     # Persisted FAISS index files
└── Capstone_Project_Maharshi.zip    # Final submission ZIP archive
```

---

## Phase-by-Phase Implementation Mapping

| Capstone Phase | Implemented Capability | Key Artefact / Script |
|---|---|---|
| **Phase 1: Problem Framing** | Problem definition, user personas, success criteria, failure modes | [`1_PROBLEM_FRAMING.md`](file:///c:/Users/Maharshi/Documents/IITM_Agentic/Week21/work/1_PROBLEM_FRAMING.md) |
| **Phase 2: Baseline Agent** | Keyword rule baseline, demonstration of 4 key limitations | [`phase2_baseline_agent.py`](file:///c:/Users/Maharshi/Documents/IITM_Agentic/Week21/work/phase2_baseline_agent.py) |
| **Phase 3: Prompt Evaluation** | 3 prompt variants benchmarked side-by-side with comparison table | [`phase3_prompt_evaluation.py`](file:///c:/Users/Maharshi/Documents/IITM_Agentic/Week21/work/phase3_prompt_evaluation.py), [`3_PROMPT_COMPARISON.md`](file:///c:/Users/Maharshi/Documents/IITM_Agentic/Week21/work/3_PROMPT_COMPARISON.md) |
| **Phase 4: Knowledge & RAG** | Ingestion of 4 policy files, 800/150 chunking, FAISS index | [`rag_engine.py`](file:///c:/Users/Maharshi/Documents/IITM_Agentic/Week21/work/rag_engine.py), [`data/`](file:///c:/Users/Maharshi/Documents/IITM_Agentic/Week21/work/data/) |
| **Phase 5: Tool Usage** | Account summary, loan EMI math, forex rates, escalation ticket | [`tools.py`](file:///c:/Users/Maharshi/Documents/IITM_Agentic/Week21/work/tools.py) |
| **Phase 6: Planning & Memory**| 4-step task decomposition, sliding window memory ($k=6$) | [`memory_and_planner.py`](file:///c:/Users/Maharshi/Documents/IITM_Agentic/Week21/work/memory_and_planner.py) |
| **Phase 7: Adaptive Behaviour**| Feedback registry, continuous prompt context adaptation | [`adaptive_engine.py`](file:///c:/Users/Maharshi/Documents/IITM_Agentic/Week21/work/adaptive_engine.py) |
| **Phase 8: Deployment & Safety**| Regex PII scrubbing, latency tracking, graceful degradation | [`safe_logger.py`](file:///c:/Users/Maharshi/Documents/IITM_Agentic/Week21/work/safe_logger.py), [`app.py`](file:///c:/Users/Maharshi/Documents/IITM_Agentic/Week21/work/app.py) |
| **Phase 9: Evaluation Review** | Test harness, root cause analysis on debugged failure case | [`run_capstone_evaluation.py`](file:///c:/Users/Maharshi/Documents/IITM_Agentic/Week21/work/run_capstone_evaluation.py), [`4_EVALUATION_REPORT.md`](file:///c:/Users/Maharshi/Documents/IITM_Agentic/Week21/work/4_EVALUATION_REPORT.md) |

---

## How to Run & Verify

### 1. Run Automated Full Capstone Evaluation
Executes all 9 scenarios, validates safety, tools, RAG, memory, PII sanitization, and saves output logs:
```powershell
cd C:\Users\Maharshi\Documents\IITM_Agentic\Week21\work
python run_capstone_evaluation.py
```

### 2. Run Prompt Engineering Benchmark (Phase 3)
```powershell
python phase3_prompt_evaluation.py
```

### 3. Launch Interactive Streamlit Web Application
```powershell
streamlit run app.py
```

### 4. Run Interactive CLI Mode
```powershell
python main.py
```

### 5. Import into Langflow
- Launch Langflow Desktop or Web (`http://127.0.0.1:7860`).
- Click **Import** and select [`apex_bank_copilot_langflow.json`](file:///c:/Users/Maharshi/Documents/IITM_Agentic/Week21/work/apex_bank_copilot_langflow.json).
- Inspect the visual pipeline nodes and connections!

