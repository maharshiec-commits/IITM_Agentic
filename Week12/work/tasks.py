"""
================================================================================
BANKING MULTI-AGENT SYSTEM — TASK DEFINITIONS
================================================================================
Defines the 4 sequential tasks that form the goal-oriented workflow.
Each task depends on the output of the previous task (handoff pattern).

Pipeline:
  Task 1 (Intent Classification) 
    → Task 2 (Policy Reasoning)   [receives Task 1 output]
    → Task 3 (Response Drafting)  [receives Task 1 + Task 2 output]
    → Task 4 (Risk & Escalation) [receives Task 1 + Task 2 + Task 3 output]
================================================================================
"""

from crewai import Task
from config.policies import (
    get_policy_text_for_category,
    ESCALATION_RULES,
)
from config.mock_data import get_customer_context


def create_intent_classification_task(agent, customer_query: str, customer_id: str) -> Task:
    """
    TASK 1: Classify the customer query.
    
    This is the entry point of the pipeline. No dependency on other tasks.
    The output must be structured so downstream agents can parse it.
    """
    customer_context = get_customer_context(customer_id)
    
    return Task(
        description=f"""Analyze the following customer query and classify it accurately.

=== CUSTOMER QUERY ===
{customer_query}

=== CUSTOMER CONTEXT ===
{customer_context}

=== YOUR TASK ===
1. Determine the PRIMARY CATEGORY: fraud | transaction | loan | card | general
2. Determine the SPECIFIC SUB-CATEGORY (e.g., "unauthorized_transaction", "failed_payment", "duplicate_charge", "card_block", "emi_issue", "loan_foreclosure", "account_statement", etc.)
3. Assess the URGENCY LEVEL: LOW | MEDIUM | HIGH | CRITICAL
   - CRITICAL: Active fraud, unauthorized access, account compromise
   - HIGH: Large financial loss, time-sensitive issues
   - MEDIUM: Service disruption, repeated complaints, moderate amounts
   - LOW: General inquiries, routine requests
4. Extract KEY ENTITIES: amounts, dates, transaction IDs, card numbers, merchant names
5. Provide a brief REASONING for your classification

You MUST output your analysis in this EXACT format:
---
CATEGORY: <category>
SUB_CATEGORY: <sub_category>
URGENCY: <LOW|MEDIUM|HIGH|CRITICAL>
ENTITIES:
  - Amount: <amount or N/A>
  - Date: <date or N/A>
  - Transaction_IDs: <ids or N/A>
  - Card_Number: <number or N/A>
  - Merchant: <merchant or N/A>
REASONING: <1-2 sentence explanation>
---""",
        expected_output=(
            "A structured classification with CATEGORY, SUB_CATEGORY, URGENCY, "
            "extracted ENTITIES, and REASONING in the exact format specified."
        ),
        agent=agent,
    )


def create_policy_reasoning_task(agent, customer_query: str, customer_id: str, context_task: Task) -> Task:
    """
    TASK 2: Apply banking policies to the classified issue.
    
    DEPENDS ON: Task 1 (Intent Classification) — uses classification output.
    """
    # Pre-load all policy categories for reference
    all_policy_text = ""
    for category in ["transaction", "fraud", "card", "loan", "general"]:
        all_policy_text += f"\n\n=== {category.upper()} POLICIES ===\n"
        all_policy_text += get_policy_text_for_category(category)
    
    escalation_text = f"""
=== ESCALATION RULES ===
High Risk Indicators (ALWAYS ESCALATE): {', '.join(ESCALATION_RULES['high_risk_indicators'])}
Medium Risk Indicators: {', '.join(ESCALATION_RULES['medium_risk_indicators'])}

Escalation Thresholds:
  - Transaction amount >= INR 1,00,000: HIGH priority
  - Transaction amount >= INR 5,00,000: CRITICAL priority
  - Failed OTP attempts >= 3: Account block
  - Days since incident > 3 and fraud-related: Increased liability

Escalation Matrix:
  CRITICAL -> Fraud Investigation Unit + Senior Manager (SLA: 1 hour)
  HIGH     -> Senior Customer Support + Department Head (SLA: 4 hours)
  MEDIUM   -> Senior Customer Support (SLA: 24 hours)
  LOW      -> Auto-resolved / L1 Support (SLA: 48 hours)
"""
    
    customer_context = get_customer_context(customer_id)
    
    return Task(
        description=f"""Based on the intent classification from the previous agent, apply the correct banking policies.

=== ORIGINAL CUSTOMER QUERY ===
{customer_query}

=== CUSTOMER CONTEXT ===
{customer_context}

=== BANKING POLICY DATABASE ===
{all_policy_text}

{escalation_text}

=== YOUR TASK ===
Using the classification output from the Intent Classification Agent:

1. Identify the APPLICABLE POLICY by its Policy ID (e.g., TXN-001, FRD-001, CRD-001, etc.)
2. List the SPECIFIC RULES that apply to this customer's situation
3. Determine if AUTO-RESOLUTION is possible (Yes/No) and why
4. State the applicable SLA (in hours)
5. Identify any RISK FLAGS based on the escalation rules
6. Recommend the RESOLUTION PATH: auto-resolve | manual-review | escalate

You MUST output your analysis in this EXACT format:
---
APPLICABLE_POLICY: <Policy ID> - <Policy Title>
APPLICABLE_RULES:
  1. <rule 1>
  2. <rule 2>
  ...
AUTO_RESOLUTION: <Yes|No>
AUTO_RESOLUTION_REASON: <explanation>
SLA_HOURS: <number>
RISK_FLAGS: <list of flags or "None">
RECOMMENDED_PATH: <auto-resolve|manual-review|escalate>
POLICY_REASONING: <2-3 sentence detailed reasoning>
---""",
        expected_output=(
            "A structured policy analysis with APPLICABLE_POLICY, APPLICABLE_RULES, "
            "AUTO_RESOLUTION decision, SLA_HOURS, RISK_FLAGS, RECOMMENDED_PATH, "
            "and POLICY_REASONING in the exact format specified."
        ),
        agent=agent,
        context=[context_task],
    )


def create_response_drafting_task(agent, customer_query: str, customer_id: str, 
                                  context_tasks: list) -> Task:
    """
    TASK 3: Draft a customer-facing response.
    
    DEPENDS ON: Task 1 (classification) + Task 2 (policy analysis)
    """
    customer_context = get_customer_context(customer_id)
    customer_name = customer_context.split("Name: ")[1].split("\n")[0] if "Name: " in customer_context else "Valued Customer"
    
    return Task(
        description=f"""Draft a professional customer response based on the intent classification and policy analysis from the previous agents.

=== ORIGINAL CUSTOMER QUERY ===
{customer_query}

=== CUSTOMER NAME ===
{customer_name}

=== CUSTOMER CONTEXT ===
{customer_context}

=== YOUR TASK ===
Using the outputs from the Intent Classification Agent AND the Policy Reasoning Agent:

1. Address the customer BY NAME
2. Acknowledge their specific concern (reference exact details they mentioned)
3. Explain what the bank will do (based on policy analysis)
4. Provide SPECIFIC TIMELINES (from SLA)
5. Include any REFERENCE NUMBERS or next steps
6. If escalation is recommended, inform the customer their case has been prioritized
7. Close with a reassuring statement

TONE GUIDELINES:
- For FRAUD cases: Urgent, reassuring, action-oriented ("We take this extremely seriously...")
- For TRANSACTION issues: Professional, solution-focused ("We've identified the issue...")
- For LOAN queries: Informative, clear ("Here's everything you need to know...")
- For CARD issues: Efficient, immediate ("We've taken immediate action...")
- For GENERAL queries: Helpful, friendly ("Here's how you can...")

IMPORTANT:
- Never promise anything outside of policy
- Always include a timeline
- For Premium customers, add a personal touch
- Generate a case reference number in format: CASE-YYYYMMDD-XXXX

Output the complete draft response that can be sent directly to the customer.""",
        expected_output=(
            "A complete, professional, empathetic customer response email/message "
            "that addresses the customer by name, references their specific issue, "
            "provides policy-based resolution steps with timelines, and includes "
            "a case reference number."
        ),
        agent=agent,
        context=context_tasks,
    )


def create_risk_escalation_task(agent, customer_query: str, customer_id: str,
                                context_tasks: list) -> Task:
    """
    TASK 4: Final risk assessment and escalation decision.
    
    DEPENDS ON: Task 1 + Task 2 + Task 3 (all previous outputs)
    This is the final decision-maker in the pipeline.
    """
    customer_context = get_customer_context(customer_id)
    
    return Task(
        description=f"""Make the FINAL escalation decision and produce the complete case resolution summary.

=== ORIGINAL CUSTOMER QUERY ===
{customer_query}

=== CUSTOMER CONTEXT ===
{customer_context}

=== ESCALATION DECISION FRAMEWORK ===
You must evaluate THREE dimensions:

1. RISK ASSESSMENT:
   - Is there potential financial loss? How much?
   - Is there regulatory/compliance concern?
   - Is the customer's account at active risk?
   
2. URGENCY ASSESSMENT:
   - Is the customer experiencing ongoing harm?
   - Is the issue time-sensitive (e.g., active fraud, expiring deadlines)?
   - Has the customer been waiting or repeated their complaint?

3. UNCERTAINTY ASSESSMENT:
   - Is the intent classification confident or ambiguous?
   - Does the situation have unusual characteristics?
   - Are there conflicting signals in the data?

ESCALATION RULES (STRICT):
- ALL fraud/unauthorized/suspicious cases → MUST escalate (CRITICAL)
- Transaction amount > INR 5,00,000 → MUST escalate (CRITICAL)
- Transaction amount > INR 1,00,000 → Escalate (HIGH)
- Customer has > 2 recent complaints → Escalate (MEDIUM)
- Loan default/hardship cases → Escalate (MEDIUM)
- Routine queries with clear policy → No escalation (LOW)

=== YOUR TASK ===
Review ALL outputs from previous agents and produce the FINAL case summary:

1. Confirm or override the RISK LEVEL: CRITICAL | HIGH | MEDIUM | LOW
2. Make the ESCALATION DECISION: ESCALATE or DO NOT ESCALATE
3. If escalating, specify the TARGET TEAM and required ACTIONS
4. APPROVE or MODIFY the drafted customer response
5. List all IMMEDIATE ACTIONS required
6. Provide the FINAL CASE SUMMARY

You MUST output in this EXACT format:
---
FINAL_RISK_LEVEL: <CRITICAL|HIGH|MEDIUM|LOW>
ESCALATION_DECISION: <ESCALATE|DO_NOT_ESCALATE>
ESCALATION_TARGET: <Team name or "N/A">
ESCALATION_SLA: <timeframe or "N/A">
ESCALATION_REASON: <reason or "N/A - Routine resolution">

IMMEDIATE_ACTIONS:
  1. <action 1>
  2. <action 2>
  ...

RESPONSE_STATUS: <APPROVED|MODIFIED>
RESPONSE_MODIFICATIONS: <modifications or "None - Response approved as drafted">

FINAL_CASE_SUMMARY:
  Case_ID: <CASE-YYYYMMDD-XXXX>
  Customer: <name>
  Category: <category>
  Risk_Level: <level>
  Resolution: <brief resolution description>
  Escalated: <Yes|No>
  SLA: <timeframe>
  Status: <Open|Resolved|Escalated>
---""",
        expected_output=(
            "A complete final case summary with FINAL_RISK_LEVEL, ESCALATION_DECISION, "
            "ESCALATION_TARGET, IMMEDIATE_ACTIONS, RESPONSE_STATUS, and a structured "
            "FINAL_CASE_SUMMARY in the exact format specified."
        ),
        agent=agent,
        context=context_tasks,
    )


def create_all_tasks(agents: dict, customer_query: str, customer_id: str) -> list:
    """
    Creates the complete sequential task pipeline.
    Returns tasks in execution order with proper handoffs.
    """
    # Task 1: Intent Classification (no dependencies)
    task1 = create_intent_classification_task(
        agent=agents["intent_classifier"],
        customer_query=customer_query,
        customer_id=customer_id,
    )
    
    # Task 2: Policy Reasoning (depends on Task 1)
    task2 = create_policy_reasoning_task(
        agent=agents["policy_reasoner"],
        customer_query=customer_query,
        customer_id=customer_id,
        context_task=task1,
    )
    
    # Task 3: Response Drafting (depends on Task 1 + Task 2)
    task3 = create_response_drafting_task(
        agent=agents["response_drafter"],
        customer_query=customer_query,
        customer_id=customer_id,
        context_tasks=[task1, task2],
    )
    
    # Task 4: Risk & Escalation (depends on Task 1 + Task 2 + Task 3)
    task4 = create_risk_escalation_task(
        agent=agents["risk_escalation"],
        customer_query=customer_query,
        customer_id=customer_id,
        context_tasks=[task1, task2, task3],
    )
    
    return [task1, task2, task3, task4]

