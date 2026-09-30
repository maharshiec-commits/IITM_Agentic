# Capstone Deliverable 1: Problem Framing Document

**Project**: ApexBank AI Advisory & Support Copilot  
**Industry Scenario**: Scenario 2 — Banking: AI Banking Support & Advisory Agent (Non-Transactional)  
**Author / Consultant**: Maharshi (Applied AI Consultant / AI Engineer)  
**Date**: September 2026  

---

## 1. Problem Statement & Business Opportunity

Retail and Commercial banking institutions handle thousands of daily customer inquiries across digital touchpoints regarding account standings, interest rate calculations, foreign currency conversions, KYC compliance, and loan terms. 

Currently, customer support incurs significant bottlenecks:
- **Human Agent Overload**: High volumes of repetitive queries (e.g. *"What is the senior citizen FD rate for 444 days?"*, *"What are the locker fees?"*, *"Calculate my loan EMI"*) consume over 40% of branch and call-center capacity.
- **Risk of Financial Misinformation**: Traditional chatbots hallucinate policies or quote obsolete interest rates, risking severe regulatory penalties from the Reserve Bank of India (RBI).
- **Unauthorized Transaction Liabilities**: An AI agent operating in banking must have ironclad boundaries to prevent money movement, unauthorized fund transfers, credential modifications, or speculative financial advice.
- **PII Leakage in Telemetry**: Customer account numbers, card credentials, and phone numbers must never be exposed or persisted in plain text logs.

**Objective**: Deploy a production-grade, non-transactional **AI Banking Support & Advisory Copilot** that automates customer advisory, grounds all responses in official regulatory policies, executes deterministic calculation and inquiry tools, escalates high-risk fraud cases within minutes, and enforces strict zero-PII logging.

---

## 2. Primary User Personas & Workflows

### Persona 1: Priya Sharma (Retail & SME Banking Customer)
- **Role**: Small business owner and retail savings customer (`CUST101`).
- **Needs**: Checks account balances, computes loan EMIs for equipment financing, checks foreign exchange conversion for international supplier invoices, and understands KYC renewal requirements.
- **Daily Workflow**: Accesses digital banking portal, asks natural-language questions, expects instant accurate numbers and policy clarity without branch visits.

### Persona 2: Rajesh Varma (High-Net-Worth / Wealth Client)
- **Role**: Premium Wealth Savings account holder (`CUST102`).
- **Needs**: Understands fixed deposit matrices, locker allocations, and urgent assistance during card compromise or suspicious transactions.
- **Workflow**: Requires immediate escalation to the Fraud Investigation Unit with formal tracking tickets when fraud occurs.

### Persona 3: Branch Relationship Managers (Internal Bank Staff)
- **Role**: Front-line advisory staff at Jubilee Hills branch.
- **Needs**: Uses the Copilot as a decision-support tool to quickly look up complex regulatory clauses (e.g. OVD list, NRE/NRO repatriation ceilings, foreclosure penalty slabs).

---

## 3. Scope, Inputs, Outputs & System Boundaries

| Attribute | Specification |
|---|---|
| **System Inputs** | Natural language text inquiries from customers via Web/Mobile/CLI interfaces. Customer ID context (`CUST101`, `CUST102`, etc.) when authenticated. |
| **System Outputs** | Factual, grounded advisory responses; deterministic EMI schedules; live forex rates; support escalation ticket IDs; clear non-transactional refusals. |
| **Out-of-Scope (Hard Boundaries)** | Executing fund transfers, altering passwords/PINs, approving loans, modifying account balances, or offering binding legal counsel. |
| **Safety Mandate** | Strict non-transactional guardrail; zero hallucination; proactive fraud escalation to 24x7 helpline `1800-APEX-SECURE`; full PII sanitization in all audit logs. |

---

## 4. Key Success Criteria & Metrics

To ensure enterprise readiness, the agent is evaluated against quantifiable engineering and business KPIs:

| Metric | Target Baseline | Capstone Target | Measurement Methodology |
|---|---|---|---|
| **Transactional Safety Rate** | 100% | **100%** | Zero money transfers or password resets executed across all red-team attempts. |
| **Factual Policy Accuracy** | < 60% (Baseline) | **> 95%** | Evaluated against verified ground truth in banking policy documents. |
| **Hallucination Rate** | > 35% (Baseline) | **< 2%** | Verification that agent refuses or states uncertainty for non-existent products. |
| **PII Redaction Efficiency** | 0% (Baseline) | **100%** | Automated regex verification that no raw card/account/phone numbers appear in audit logs. |
| **Multi-Turn Context Retention** | 0% (Baseline) | **> 90%** | Successful resolution of pronouns and follow-up constraints across 3+ conversation turns. |
| **Average Response Latency** | N/A | **< 3.5 seconds** | End-to-end processing time including RAG search and tool execution. |

---

## 5. Anticipated Failures & Mitigation Strategies

| Anticipated Failure Mode | Potential Impact | Engineering Mitigation |
|---|---|---|
| **1. Prompt Injection for Fund Transfer** | Critical security violation: Customer tricks LLM into "simulating" or triggering a fund transfer. | Multi-layered safety interceptor: Deterministic intent regex firewall blocks requests before LLM invocation, reinforced by system prompt instructions. |
| **2. Hallucinating Obsolete Deposit Rates** | Customer acts on false interest rates, leading to financial disputes and regulatory fines. | Vector RAG architecture: Dense embeddings retrieve the authoritative, active policy document (`loan_and_interest_terms.txt`) at runtime. |
| **3. Inaccurate EMI Math** | LLMs cannot reliably perform complex compound interest formulas. | Dedicated Deterministic Tool: Offloads all EMI math to `calculate_loan_emi()` executing exact reducing-balance formulas. |
| **4. PII Exposure in Telemetry** | Storing customer card or account numbers in application logs violates RBI and DPDP regulations. | Automated PII Sanitization Engine: Regex-based scrubber masks credit cards, accounts, Aadhaar, and phone numbers prior to disk persistence. |
| **5. Unresolved Fraud Panic** | Customer reporting a stolen card receives generic advice, resulting in unauthorized losses. | Automatic Escalation Tool: Automatically generates a formal grievance ticket assigned to the Fraud Investigation Unit with emergency hotline numbers. |

