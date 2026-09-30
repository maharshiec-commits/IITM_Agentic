# Architecture Explanation: Banking Multi-Agent Intelligent Customer Resolution

**Course**: IITM Pravartak — Week 12 Graded Mini Project  
**Use Case**: Banking & Financial Services — Intelligent Customer Resolution  
**Framework**: CrewAI (Sequential Goal-Oriented Multi-Agent Flow)  
**Author**: Maharshi  
**Date**: September 2026

---

## 1. System Overview

This project implements a **goal-oriented multi-agent system** that handles customer queries in a banking context. The system receives a customer message (e.g., fraud report, failed transaction, loan inquiry), routes it through 4 specialized agents in a strict sequential pipeline, and produces: (a) a policy-compliant customer response, and (b) an escalation decision with risk assessment.

The architecture mirrors real-world banking customer support triage, where a query is classified, policy-checked, a response is drafted, and a risk officer reviews the case before dispatch.

---

## 2. Agent Roles & Responsibilities

| # | Agent | Role | Goal | Key Inputs | Key Outputs |
|---|-------|------|------|-----------|-------------|
| 1 | **Intent Classification Agent** | Senior Banking Intent Classification Specialist | Classify query into `fraud`, `transaction`, `loan`, `card`, or `general`; determine urgency; extract entities | Raw customer message + customer profile | Category, sub-category, urgency level (LOW/MEDIUM/HIGH/CRITICAL), extracted entities |
| 2 | **Policy Reasoning Agent** | Banking Policy & Compliance Expert | Apply correct banking policies, determine auto-resolution feasibility, identify risk flags | Classification from Agent 1 + full policy database | Applicable policy ID, specific rules, SLA, risk flags, recommended resolution path |
| 3 | **Response Drafting Agent** | Senior Customer Communications Specialist | Generate empathetic, accurate, policy-compliant customer response with timelines and reference numbers | Classification + policy analysis + customer context | Professional customer response ready for delivery |
| 4 | **Risk & Escalation Agent** | Chief Risk & Escalation Decision Officer | Final escalation decision based on risk, urgency, and uncertainty; approve or modify drafted response | All outputs from Agents 1-3 | Final risk level, escalation decision, target team, approved response, case summary |

---

## 3. Task Flow & Handoffs

The agents operate in a **strictly sequential pipeline** enforced by CrewAI's `Process.sequential` mode:

```
Customer Query
     │
     ▼
┌─────────────────────────────────┐
│  AGENT 1: Intent Classification │ ← Customer message + profile
│  Output: Category, Urgency,     │
│          Entities                │
└──────────────┬──────────────────┘
               │ handoff (Task 1 output)
               ▼
┌─────────────────────────────────┐
│  AGENT 2: Policy Reasoning      │ ← Task 1 output + Policy DB
│  Output: Applicable policy,     │
│          Rules, SLA, Risk flags  │
└──────────────┬──────────────────┘
               │ handoff (Task 1 + Task 2 output)
               ▼
┌─────────────────────────────────┐
│  AGENT 3: Response Drafting     │ ← Task 1 + Task 2 output + Customer name
│  Output: Customer-facing        │
│          response draft          │
└──────────────┬──────────────────┘
               │ handoff (Task 1 + Task 2 + Task 3 output)
               ▼
┌─────────────────────────────────┐
│  AGENT 4: Risk & Escalation     │ ← ALL prior outputs
│  Output: Final decision,        │
│          Approved response,      │
│          Case summary            │
└──────────────┬──────────────────┘
               │
               ▼
        Final Resolution
    (Response + Escalation Action)
```

### Handoff Mechanism
- CrewAI's `context` parameter on each Task defines which prior task outputs are injected into the agent's prompt.
- Task 2 receives Task 1's output via `context=[task1]`.
- Task 3 receives both Task 1 and Task 2 outputs via `context=[task1, task2]`.
- Task 4 receives all three via `context=[task1, task2, task3]`.
- Each agent produces **structured output** in a predefined format, ensuring downstream agents can reliably parse the handoff.

---

## 4. Escalation Logic

Escalation is **not a vague decision** — it follows explicit, deterministic rules evaluated by the Risk & Escalation Agent:

### Escalation Triggers (Strict Rules)

| Condition | Risk Level | Escalation |
|-----------|-----------|------------|
| ANY fraud/unauthorized/suspicious/phishing keyword | **CRITICAL** | ✅ Always escalate to Fraud Investigation Unit |
| Transaction amount ≥ ₹5,00,000 | **CRITICAL** | ✅ Escalate to Fraud Unit + Senior Manager |
| Transaction amount ≥ ₹1,00,000 | **HIGH** | ✅ Escalate to Senior Support + Dept Head |
| Customer has >2 recent complaints | **MEDIUM** | ✅ Escalate to Senior Support |
| Loan default / hardship case | **MEDIUM** | ✅ Escalate for restructuring review |
| Routine query with clear policy match | **LOW** | ❌ Auto-resolve via L1 Support |

### Three-Pillar Decision Framework
The Risk Agent evaluates every case on three dimensions:
1. **Risk**: Potential financial loss or regulatory concern?
2. **Urgency**: Customer at active risk right now?
3. **Uncertainty**: Is the classification confident or ambiguous?

### Escalation Matrix

| Level | Target Team | SLA | Actions |
|-------|------------|-----|---------|
| CRITICAL | Fraud Investigation Unit + Senior Manager | 1 hour | Immediate account freeze, SAR filing, callback |
| HIGH | Senior Support + Department Head | 4 hours | Priority queue, supervisor review |
| MEDIUM | Senior Customer Support | 24 hours | Specialist assignment |
| LOW | Auto-resolved / L1 Support | 48 hours | Standard process, self-service |

---

## 5. Sample Inputs & Expected Outputs

### Query 1 — Duplicate Charge (Routine, LOW risk)
- **Input**: _"I was charged twice for the same Amazon order of Rs 4,500 on September 25th. Please refund the duplicate charge."_ (Customer: CUST001)
- **Expected Classification**: `transaction` / `duplicate_charge` / `LOW`
- **Expected Policy**: TXN-002 (Duplicate Transaction Charge Policy) — auto-resolution eligible
- **Expected Escalation**: ❌ No escalation. Auto-refund within 3-5 business days.

### Query 3 — Unauthorized Transactions (CRITICAL escalation)
- **Input**: _"I did NOT make these transactions! Three large transfers totalling over 5 lakhs to unknown vendors from Delhi, Singapore and London in the last 24 hours. This is FRAUD!"_ (Customer: CUST003)
- **Expected Classification**: `fraud` / `unauthorized_transaction` / `CRITICAL`
- **Expected Policy**: FRD-001 (Unauthorized Transaction Policy) — MUST escalate, zero liability if reported in 3 days
- **Expected Escalation**: ✅ CRITICAL → Fraud Investigation Unit. Immediate account freeze, SAR filing.

### Query 4 — EMI Bounce (MEDIUM)
- **Input**: _"My personal loan EMI of Rs 12,000 was not deducted on September 20th due to insufficient balance. Will there be a late fee? Will it affect my CIBIL score?"_ (Customer: CUST004)
- **Expected Classification**: `loan` / `emi_issue` / `MEDIUM`
- **Expected Policy**: LN-002 — 3-day grace period, 2% late fee, CIBIL notification
- **Expected Escalation**: Possible MEDIUM escalation (depends on days elapsed, hardship assessment).

### Query 6 — Phishing Victim (CRITICAL escalation)
- **Input**: _"Someone called me claiming to be from the bank and I accidentally shared my OTP. Now I see Rs 8,000 debited."_ (Customer: CUST002)
- **Expected Classification**: `fraud` / `phishing_report` / `CRITICAL`
- **Expected Policy**: FRD-002 — Liability shifts to customer if OTP shared voluntarily, but immediate card block and escalation required
- **Expected Escalation**: ✅ CRITICAL → Fraud team for account monitoring.

---

## 6. Design Rationale

### Why Sequential (not Parallel)?
Banking customer resolution requires **strict information dependency**. The policy agent cannot reason without knowing the category. The response agent cannot draft without knowing the applicable rules. The risk agent must see everything before making the final call. Sequential execution guarantees correctness.

### Why Static Policies Instead of RAG?
Per project requirements, RAG is not required. Static policies (`config/policies.py`) simulate a real policy database with:
- Structured policy IDs, rules, SLAs, and auto-resolution flags
- Escalation thresholds with numeric boundaries (amounts, time limits)
- This approach is deterministic, testable, and transparent

### Why a Separate Risk Agent (Agent 4)?
Separation of concerns: The policy agent determines *what the rules say*. The risk agent determines *what to do about it*. This mirrors real banking organizations where compliance and risk management are separate functions. It also prevents a single agent from both interpreting policy AND deciding escalation, which could lead to bias.

### Why Structured Output Formats?
Each agent is instructed to produce output in a strict `KEY: value` format. This ensures:
- Reliable parsing by downstream agents
- Clear audit trail for compliance
- Easy automated testing of classification accuracy

---

## 7. Project Structure

```
Week12/work/
├── main.py                     # Main orchestrator (runs multiple queries)
├── run_single_query.py         # Quick single-query runner for testing
├── agents.py                   # 4 Agent definitions (roles, goals, backstories)
├── tasks.py                    # 4 Task definitions (prompts, handoffs, context)
├── requirements.txt            # Python dependencies
├── .env                        # LLM API key configuration
├── architecture.md             # This document
├── config/
│   ├── __init__.py
│   ├── policies.py             # Static banking policies & escalation rules
│   └── mock_data.py            # Mock customers, transactions, sample queries
└── output_results_*.json       # Saved execution results (generated at runtime)
```

---

## 8. How to Run

```bash
# Install dependencies
pip install crewai crewai-tools python-dotenv

# Set API key in .env
echo GOOGLE_API_KEY=your-key-here > .env

# Run a single query (quick test)
python run_single_query.py Q1

# Run the full demo (5 diverse queries)
python main.py

# Run specific queries
python main.py Q3 Q6

# Run with custom interactive input
python run_single_query.py --custom
```

