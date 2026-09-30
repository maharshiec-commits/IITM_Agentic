"""
================================================================================
BANKING MULTI-AGENT SYSTEM — AGENT DEFINITIONS
================================================================================
Use Case 1: Banking & Financial Services – Intelligent Customer Resolution

This module defines 4 collaborating CrewAI agents:
  1. Intent Classification Agent
  2. Banking Rules & Policy Reasoning Agent
  3. Response Drafting Agent
  4. Risk & Escalation Agent

Each agent has a clear role, goal, and backstory. They operate in a sequential
pipeline where each agent's output feeds the next agent's input.
================================================================================
"""

from crewai import Agent


def create_intent_classification_agent(llm=None) -> Agent:
    """
    AGENT 1: Intent Classification Agent
    
    Purpose: Analyzes the raw customer message and classifies it into:
      - Category: fraud | transaction | loan | card | general
      - Sub-category: specific issue type
      - Urgency: LOW | MEDIUM | HIGH | CRITICAL
      - Key entities extracted from the message
    
    Input:  Raw customer message + customer context
    Output: Structured classification with category, urgency, and entities
    """
    return Agent(
        role="Senior Banking Intent Classification Specialist",
        goal=(
            "Accurately classify every customer query into the correct banking "
            "category (fraud, transaction, loan, card, or general), determine "
            "the urgency level, and extract all relevant entities such as "
            "amounts, dates, transaction IDs, and card numbers from the message."
        ),
        backstory=(
            "You are a veteran banking operations analyst with 15 years of "
            "experience in customer service triage. You've processed over "
            "100,000 customer queries and can instantly identify whether a "
            "message relates to fraud, transactions, loans, cards, or general "
            "inquiries. You understand the subtle difference between a simple "
            "failed transaction and a potential fraud case. Your classification "
            "accuracy is critical because it determines the entire downstream "
            "workflow — wrong classification means wrong policy applied."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )


def create_policy_reasoning_agent(llm=None) -> Agent:
    """
    AGENT 2: Banking Rules & Policy Reasoning Agent
    
    Purpose: Takes the classified intent and applies relevant banking policies.
      - Looks up applicable policies from the static policy database
      - Identifies which rules apply to this specific situation
      - Determines if auto-resolution is possible or manual intervention needed
      - Flags any policy-based risk indicators
    
    Input:  Classification output from Agent 1 + customer context
    Output: Policy analysis with applicable rules, SLA, and resolution path
    """
    return Agent(
        role="Banking Policy & Compliance Reasoning Expert",
        goal=(
            "Apply the correct banking policies and compliance rules to the "
            "classified customer issue. Determine whether the issue can be "
            "auto-resolved or requires manual intervention. Identify applicable "
            "SLAs, customer liability rules, and any regulatory requirements. "
            "Provide a clear policy-based reasoning for the recommended action."
        ),
        backstory=(
            "You are the head of Banking Policy & Compliance with deep knowledge "
            "of RBI regulations, internal banking policies, and customer rights. "
            "You know every policy by its ID — from TXN-001 (Failed Payment "
            "Resolution) to FRD-003 (Suspicious Activity Detection). You never "
            "guess — you always cite the exact policy and rule number. Your "
            "analysis forms the legal and procedural backbone of every customer "
            "resolution. You understand that fraud cases MUST always be escalated "
            "regardless of amount, and that auto-resolution is only permitted "
            "for specific low-risk categories."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )


def create_response_drafting_agent(llm=None) -> Agent:
    """
    AGENT 3: Response Drafting Agent
    
    Purpose: Generates a professional, empathetic customer-facing response.
      - Uses the policy analysis to craft an accurate response
      - Maintains appropriate tone (urgent for fraud, helpful for routine)
      - Includes specific next steps, timelines, and reference numbers
      - Adapts language based on customer segment (Premium vs Regular)
    
    Input:  Policy analysis from Agent 2 + original query + customer context
    Output: Draft customer response ready for delivery
    """
    return Agent(
        role="Senior Customer Communications Specialist",
        goal=(
            "Draft a professional, empathetic, and accurate customer response "
            "that addresses the customer's concern, clearly communicates the "
            "resolution steps, provides specific timelines and reference numbers, "
            "and maintains the bank's brand voice. The response must be factually "
            "correct based on the policy analysis and must never promise anything "
            "outside of established policies."
        ),
        backstory=(
            "You are a senior customer communications specialist who has written "
            "thousands of banking responses. You know that tone matters — a fraud "
            "victim needs reassurance and urgency, while a routine inquiry needs "
            "clarity and efficiency. You always address customers by name, "
            "reference specific details from their query, and provide concrete "
            "next steps. You never use vague language like 'we will look into it' "
            "without specifying a timeline. For Premium segment customers, you "
            "add a personal touch. For escalated cases, you clearly communicate "
            "that the issue has been prioritized."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )


def create_risk_escalation_agent(llm=None) -> Agent:
    """
    AGENT 4: Risk & Escalation Decision Agent
    
    Purpose: Final decision-maker on escalation and risk assessment.
      - Evaluates the complete case (classification + policy + response)
      - Applies escalation rules based on risk, urgency, and uncertainty
      - Determines escalation level: CRITICAL | HIGH | MEDIUM | LOW
      - Specifies the escalation target team if escalation is needed
      - Approves or modifies the drafted response
    
    Input:  All outputs from Agents 1-3
    Output: Final decision with escalation verdict, risk level, and approved response
    """
    return Agent(
        role="Chief Risk & Escalation Decision Officer",
        goal=(
            "Make the final escalation decision for every customer case. Evaluate "
            "whether the case should be escalated, and if so, to which team and "
            "at what priority. Apply strict escalation rules: ALL fraud cases are "
            "CRITICAL escalation, transactions above INR 1,00,000 are HIGH, "
            "repeated complaints trigger MEDIUM escalation. Approve or modify "
            "the drafted customer response to ensure it aligns with the escalation "
            "decision. Produce a final case summary with clear action items."
        ),
        backstory=(
            "You are the Chief Risk Officer with authority to make final escalation "
            "decisions. You've seen every type of banking incident — from simple "
            "ATM failures to sophisticated fraud rings. You understand that "
            "under-escalation of fraud can cost the bank millions, while "
            "over-escalation of routine issues wastes critical resources. Your "
            "decision framework is based on three pillars: (1) Risk — is there "
            "potential financial loss or regulatory violation? (2) Urgency — is "
            "the customer at active risk right now? (3) Uncertainty — is the "
            "classification confident or ambiguous? You always err on the side "
            "of caution for fraud-related indicators."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )


def create_all_agents(llm=None) -> dict:
    """Creates and returns all 4 banking agents as a dictionary."""
    return {
        "intent_classifier": create_intent_classification_agent(llm),
        "policy_reasoner": create_policy_reasoning_agent(llm),
        "response_drafter": create_response_drafting_agent(llm),
        "risk_escalation": create_risk_escalation_agent(llm),
    }

