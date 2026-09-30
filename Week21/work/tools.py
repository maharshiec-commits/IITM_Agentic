"""
================================================================================
APEX GLOBAL BANK — TOOLS & FUNCTION CALLING ENGINE (tools.py)
================================================================================
Phase 5: Enable Tool Usage
Defines deterministic banking operations tools, Pydantic schemas, and safety
guardrails against unauthorized money movement or data modifications.
================================================================================
"""

import json
from datetime import datetime
from pydantic import BaseModel, Field

# Mock Customer Database for Non-Transactional Lookup
MOCK_CUSTOMERS = {
    "CUST101": {
        "customer_id": "CUST101",
        "name": "Priya Sharma",
        "account_type": "Classic Savings",
        "masked_account": "XXXX-XXXX-4819",
        "balance_inr": 84500.0,
        "kyc_status": "Verified (Valid till 2029)",
        "risk_tier": "Low",
        "active_loans": [{"type": "Personal Loan", "outstanding": 150000.0, "monthly_emi": 8200.0}]
    },
    "CUST102": {
        "customer_id": "CUST102",
        "name": "Rajesh Varma",
        "account_type": "Premium Wealth Savings",
        "masked_account": "XXXX-XXXX-9921",
        "balance_inr": 620000.0,
        "kyc_status": "Pending Re-KYC (High Risk)",
        "risk_tier": "High",
        "active_loans": [{"type": "Home Loan", "outstanding": 4200000.0, "monthly_emi": 38400.0}]
    },
    "CUST103": {
        "customer_id": "CUST103",
        "name": "Sneha Patel",
        "account_type": "Business Current Account",
        "masked_account": "XXXX-XXXX-3341",
        "balance_inr": 295000.0,
        "kyc_status": "Verified (Valid till 2031)",
        "risk_tier": "Low",
        "active_loans": []
    }
}

# Live Foreign Exchange Reference Rates (Base: INR)
FOREX_RATES = {
    "USD/INR": {"rate": 84.15, "last_updated": "2026-09-27 10:00 AM IST"},
    "EUR/INR": {"rate": 91.80, "last_updated": "2026-09-27 10:00 AM IST"},
    "GBP/INR": {"rate": 109.50, "last_updated": "2026-09-27 10:00 AM IST"},
    "AED/INR": {"rate": 22.91, "last_updated": "2026-09-27 10:00 AM IST"},
    "SGD/INR": {"rate": 64.75, "last_updated": "2026-09-27 10:00 AM IST"}
}


# ──────────────────────────────────────────────────────────────────────────────
# TOOL 1: ACCOUNT SUMMARY LOOKUP (READ-ONLY)
# ──────────────────────────────────────────────────────────────────────────────
def check_account_summary(customer_id: str) -> str:
    """
    Retrieves read-only account summary and KYC compliance standing for a customer ID.
    Does not expose sensitive raw PII or credentials.
    """
    cid = customer_id.strip().upper()
    if cid not in MOCK_CUSTOMERS:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Customer ID '{customer_id}' not found in Apex Bank core records."
        })
    
    data = MOCK_CUSTOMERS[cid]
    return json.dumps({
        "status": "SUCCESS",
        "customer_name": data["name"],
        "account_number": data["masked_account"],
        "account_type": data["account_type"],
        "available_balance_inr": data["balance_inr"],
        "kyc_status": data["kyc_status"],
        "active_loans": data["active_loans"]
    })


# ──────────────────────────────────────────────────────────────────────────────
# TOOL 2: LOAN EMI CALCULATOR (DETERMINISTIC REDUCING BALANCE MATH)
# ──────────────────────────────────────────────────────────────────────────────
def calculate_loan_emi(principal: float, annual_interest_rate: float, tenure_months: int) -> str:
    """
    Calculates monthly reducing-balance EMI and total interest payable.
    Formula: EMI = [P x r x (1+r)^n] / [(1+r)^n - 1]
    """
    try:
        principal = float(principal)
        annual_rate = float(annual_interest_rate)
        tenure = int(tenure_months)

        if principal <= 0 or annual_rate <= 0 or tenure <= 0:
            return json.dumps({
                "status": "INVALID_INPUT",
                "error": "Principal, interest rate, and tenure must all be positive numerical values."
            })

        monthly_rate = (annual_rate / 12) / 100.0
        numerator = principal * monthly_rate * ((1 + monthly_rate) ** tenure)
        denominator = ((1 + monthly_rate) ** tenure) - 1
        emi = numerator / denominator

        total_payment = emi * tenure
        total_interest = total_payment - principal

        return json.dumps({
            "status": "SUCCESS",
            "principal_inr": round(principal, 2),
            "annual_interest_rate_percent": round(annual_rate, 2),
            "tenure_months": tenure,
            "monthly_emi_inr": round(emi, 2),
            "total_interest_inr": round(total_interest, 2),
            "total_amount_payable_inr": round(total_payment, 2)
        })
    except Exception as e:
        return json.dumps({"status": "CALCULATION_ERROR", "error": str(e)})


# ──────────────────────────────────────────────────────────────────────────────
# TOOL 3: FOREX RATE INQUIRY
# ──────────────────────────────────────────────────────────────────────────────
def get_forex_rates(currency_pair: str) -> str:
    """
    Returns the real-time foreign currency exchange rate against INR.
    Example pairs: USD/INR, EUR/INR, GBP/INR, AED/INR, SGD/INR.
    """
    pair = currency_pair.strip().upper().replace(" ", "")
    if "/" not in pair and len(pair) == 6:
        pair = f"{pair[:3]}/{pair[3:]}"

    if pair in FOREX_RATES:
        info = FOREX_RATES[pair]
        return json.dumps({
            "status": "SUCCESS",
            "currency_pair": pair,
            "exchange_rate": info["rate"],
            "unit": f"1 {pair.split('/')[0]} = {info['rate']} INR",
            "timestamp": info["last_updated"],
            "notes": "Indicative counter rate. Standard 3.50% forex markup applies on international card transactions."
        })
    else:
        return json.dumps({
            "status": "UNSUPPORTED_PAIR",
            "message": f"Currency pair '{currency_pair}' is not supported. Supported pairs: {list(FOREX_RATES.keys())}"
        })


# ──────────────────────────────────────────────────────────────────────────────
# TOOL 4: SUPPORT ESCALATION TICKET CREATOR
# ──────────────────────────────────────────────────────────────────────────────
def create_support_escalation_ticket(customer_id: str, category: str, urgency: str, summary: str) -> str:
    """
    Generates an official bank grievance/escalation ticket assigned to human managers.
    Used for fraud, unauthorized transactions, complaints, or complex requests.
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    import random
    ticket_id = f"TKT-{timestamp}-{random.randint(1000, 9999)}"

    return json.dumps({
        "status": "TICKET_CREATED",
        "ticket_id": ticket_id,
        "customer_id": customer_id.upper(),
        "category": category,
        "urgency_level": urgency.upper(),
        "summary": summary,
        "assigned_to": "Fraud Investigation Unit" if "fraud" in category.lower() else "Senior Customer Support Manager",
        "sla_resolution_hours": 4 if urgency.upper() in ["CRITICAL", "HIGH"] else 24,
        "created_at": datetime.now().isoformat()
    })


# ──────────────────────────────────────────────────────────────────────────────
# SAFETY GUARDRAIL: PROHIBITED ACTIONS INTERCEPTOR
# ──────────────────────────────────────────────────────────────────────────────
PROHIBITED_INTENTS = [
    "transfer money", "move funds", "send money", "transfer funds", "initiate transfer",
    "wire funds", "approve loan", "disburse loan", "reset password", "change pin",
    "bypass kyc", "delete transaction", "modify balance"
]


def check_action_safety(intent_text: str) -> tuple[bool, str]:
    """
    Safety Guardrail: Evaluates whether an attempted user request or action violates
    the Non-Transactional Banking Advisory mandate.
    Returns: (is_safe: bool, refusal_explanation: str)
    """
    text_lower = intent_text.lower()
    for prohibited in PROHIBITED_INTENTS:
        if prohibited in text_lower:
            return False, (
                f"SAFETY REFUSAL: As Apex Bank's AI Advisory Copilot, I am strictly a non-transactional "
                f"advisory agent. I cannot execute financial transactions, move funds, approve credit, or alter account credentials. "
                f"For your safety, please log into Apex Online Banking or visit your nearest branch."
            )
    return True, ""


# Tool Schemas for LangChain / LLM Binding
TOOLS_METADATA = [
    {
        "name": "check_account_summary",
        "description": "Look up account balances, account type, and KYC status for a customer ID (e.g. CUST101).",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string", "description": "The customer identifier, e.g. CUST101"}
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "calculate_loan_emi",
        "description": "Calculate precise monthly EMI and total interest for a loan amount, annual rate, and tenure.",
        "parameters": {
            "type": "object",
            "properties": {
                "principal": {"type": "number", "description": "Principal loan amount in INR"},
                "annual_interest_rate": {"type": "number", "description": "Annual interest rate percentage, e.g. 8.5"},
                "tenure_months": {"type": "integer", "description": "Loan duration in months, e.g. 240"}
            },
            "required": ["principal", "annual_interest_rate", "tenure_months"]
        }
    },
    {
        "name": "get_forex_rates",
        "description": "Fetch real-time foreign currency exchange rate against INR (e.g. USD/INR, EUR/INR, GBP/INR).",
        "parameters": {
            "type": "object",
            "properties": {
                "currency_pair": {"type": "string", "description": "Currency pair symbol like USD/INR or GBP/INR"}
            },
            "required": ["currency_pair"]
        }
    },
    {
        "name": "create_support_escalation_ticket",
        "description": "Create an official human escalation ticket for fraud, disputes, high-risk, or unresolved complaints.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string", "description": "Customer ID filing the issue"},
                "category": {"type": "string", "description": "Dispute category, e.g., Fraud, KYC, Dispute, Loan"},
                "urgency": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"]},
                "summary": {"type": "string", "description": "Brief factual summary of the grievance"}
            },
            "required": ["customer_id", "category", "urgency", "summary"]
        }
    }
]

