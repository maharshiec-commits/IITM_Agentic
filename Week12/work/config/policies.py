"""
================================================================================
BANKING POLICIES & RULES ENGINE
================================================================================
Static banking policies used by the Policy Reasoning Agent.
These simulate the knowledge base that would normally come from a database or
document store. RAG is NOT required — all rules are hardcoded here.
================================================================================
"""

# ──────────────────────────────────────────────────────────────────────────────
# TRANSACTION POLICIES
# ──────────────────────────────────────────────────────────────────────────────
TRANSACTION_POLICIES = {
    "failed_payment": {
        "policy_id": "TXN-001",
        "title": "Failed Payment Resolution Policy",
        "rules": [
            "If the transaction status is 'failed' and amount was debited, initiate auto-reversal within 5-7 business days.",
            "If the reversal is not reflected after 7 business days, escalate to the Payments Operations team.",
            "For UPI transactions, check with NPCI settlement records.",
            "For card transactions, verify with the acquiring bank.",
            "Customers can raise a dispute within 30 days of the transaction date."
        ],
        "auto_resolution": True,
        "sla_hours": 48
    },
    "duplicate_charge": {
        "policy_id": "TXN-002",
        "title": "Duplicate Transaction Charge Policy",
        "rules": [
            "Verify if two transactions with the same amount occurred within a 5-minute window.",
            "If confirmed duplicate, initiate immediate refund for the second transaction.",
            "If the merchant confirms only one charge, process refund within 3-5 business days.",
            "Customer must provide transaction reference numbers for both charges."
        ],
        "auto_resolution": True,
        "sla_hours": 72
    },
    "international_transaction": {
        "policy_id": "TXN-003",
        "title": "International Transaction Policy",
        "rules": [
            "International transactions require prior activation of international usage on the card.",
            "A forex markup of 3.5% is applied on all international transactions.",
            "Dynamic currency conversion charges are borne by the customer.",
            "Disputes on international transactions take 45-60 business days for resolution."
        ],
        "auto_resolution": False,
        "sla_hours": 120
    }
}

# ──────────────────────────────────────────────────────────────────────────────
# FRAUD POLICIES
# ──────────────────────────────────────────────────────────────────────────────
FRAUD_POLICIES = {
    "unauthorized_transaction": {
        "policy_id": "FRD-001",
        "title": "Unauthorized Transaction Policy",
        "rules": [
            "IMMEDIATELY block the card/account upon fraud report.",
            "Initiate investigation within 24 hours of complaint.",
            "If reported within 3 days: zero liability for customer.",
            "If reported between 4-7 days: customer liability capped at INR 25,000.",
            "If reported after 7 days: liability determined case-by-case.",
            "File a Suspicious Activity Report (SAR) with the fraud department.",
            "All fraud cases MUST be escalated to the Fraud Investigation Unit."
        ],
        "auto_resolution": False,
        "sla_hours": 24,
        "always_escalate": True
    },
    "phishing_report": {
        "policy_id": "FRD-002",
        "title": "Phishing & Social Engineering Policy",
        "rules": [
            "If customer shared OTP/CVV voluntarily, liability shifts to customer.",
            "Advise immediate password change and card block.",
            "Report the phishing source to the cybercrime cell.",
            "Provide customer with incident reference number.",
            "Escalate to fraud team for account monitoring."
        ],
        "auto_resolution": False,
        "sla_hours": 24,
        "always_escalate": True
    },
    "suspicious_activity": {
        "policy_id": "FRD-003",
        "title": "Suspicious Activity Detection Policy",
        "rules": [
            "Multiple transactions from different geographies within 1 hour: FLAG.",
            "Transaction amount exceeding 5x average spending pattern: FLAG.",
            "Multiple failed OTP attempts (>3): temporarily block account.",
            "Unusual merchant category for the customer profile: FLAG.",
            "All flagged activities must be reviewed by the Fraud team within 4 hours."
        ],
        "auto_resolution": False,
        "sla_hours": 4,
        "always_escalate": True
    }
}

# ──────────────────────────────────────────────────────────────────────────────
# CARD POLICIES
# ──────────────────────────────────────────────────────────────────────────────
CARD_POLICIES = {
    "card_block": {
        "policy_id": "CRD-001",
        "title": "Card Block/Unblock Policy",
        "rules": [
            "Temporary card block can be done instantly via the mobile app or IVR.",
            "Permanent card block requires identity verification (last 4 digits of card + DOB).",
            "Replacement card is dispatched within 7-10 business days.",
            "Express delivery available in metro cities (2-3 business days) for INR 500 fee.",
            "Virtual card can be issued instantly as interim solution."
        ],
        "auto_resolution": True,
        "sla_hours": 1
    },
    "card_limit": {
        "policy_id": "CRD-002",
        "title": "Card Limit Modification Policy",
        "rules": [
            "Daily transaction limit can be modified up to the maximum eligible limit.",
            "ATM withdrawal limit: max INR 1,00,000 per day.",
            "POS/Online limit: based on card type and customer segment.",
            "Temporary limit enhancement available for 48 hours upon request.",
            "Permanent limit increase requires income document verification."
        ],
        "auto_resolution": True,
        "sla_hours": 2
    }
}

# ──────────────────────────────────────────────────────────────────────────────
# LOAN POLICIES
# ──────────────────────────────────────────────────────────────────────────────
LOAN_POLICIES = {
    "loan_status": {
        "policy_id": "LN-001",
        "title": "Loan Application Status Policy",
        "rules": [
            "Personal loan applications are processed within 3-5 business days.",
            "Home loan applications require 15-20 business days for processing.",
            "Document verification is the most common reason for delays.",
            "Customer can check real-time status via online banking portal.",
            "If pending beyond SLA, escalate to loan processing department."
        ],
        "auto_resolution": True,
        "sla_hours": 120
    },
    "emi_issue": {
        "policy_id": "LN-002",
        "title": "EMI Payment Issue Policy",
        "rules": [
            "Failed EMI auto-debit: customer has a 3-day grace period to make manual payment.",
            "Late payment fee: 2% of EMI amount or INR 500, whichever is higher.",
            "If EMI bounces 3 consecutive times, loan restructuring may be offered.",
            "CIBIL score impact notification must be sent to customer.",
            "Hardship cases (job loss, medical emergency) can request moratorium — requires escalation."
        ],
        "auto_resolution": False,
        "sla_hours": 24
    },
    "loan_foreclosure": {
        "policy_id": "LN-003",
        "title": "Loan Foreclosure Policy",
        "rules": [
            "Personal loans can be foreclosed after 12 EMIs with 4% foreclosure charge.",
            "Home loans: no foreclosure charge on floating rate loans (RBI mandate).",
            "Foreclosure statement generated within 15 business days of request.",
            "Outstanding principal + accrued interest + charges = total settlement amount.",
            "NOC issued within 30 days of full settlement."
        ],
        "auto_resolution": False,
        "sla_hours": 48
    }
}

# ──────────────────────────────────────────────────────────────────────────────
# GENERAL BANKING POLICIES
# ──────────────────────────────────────────────────────────────────────────────
GENERAL_POLICIES = {
    "account_statement": {
        "policy_id": "GEN-001",
        "title": "Account Statement Request Policy",
        "rules": [
            "E-statements available for download from net banking (last 6 months free).",
            "Physical statements: INR 100 per copy, dispatched within 5 business days.",
            "Statements older than 2 years require branch visit and INR 500 retrieval fee."
        ],
        "auto_resolution": True,
        "sla_hours": 4
    },
    "account_update": {
        "policy_id": "GEN-002",
        "title": "Account Details Update Policy",
        "rules": [
            "Address/phone update: can be done via net banking with Aadhaar OTP verification.",
            "Name change: requires branch visit with gazette notification or court order.",
            "Nominee update: can be done online or at branch with proper documentation.",
            "PAN linking: mandatory for accounts with transactions > INR 50,000."
        ],
        "auto_resolution": True,
        "sla_hours": 24
    }
}

# ──────────────────────────────────────────────────────────────────────────────
# ESCALATION RULES
# ──────────────────────────────────────────────────────────────────────────────
ESCALATION_RULES = {
    "high_risk_indicators": [
        "fraud",
        "unauthorized",
        "suspicious",
        "phishing",
        "identity theft",
        "account takeover",
        "money laundering"
    ],
    "medium_risk_indicators": [
        "large_amount",
        "international",
        "loan_default",
        "repeated_complaint",
        "regulatory"
    ],
    "escalation_thresholds": {
        "transaction_amount_high": 100000,   # INR 1 lakh
        "transaction_amount_critical": 500000,  # INR 5 lakhs
        "failed_attempts_threshold": 3,
        "days_since_incident_urgency": 3
    },
    "escalation_matrix": {
        "CRITICAL": {
            "team": "Fraud Investigation Unit + Senior Manager",
            "sla": "1 hour",
            "actions": ["Immediate account freeze", "SAR filing", "Customer callback within 1 hour"]
        },
        "HIGH": {
            "team": "Senior Customer Support + Department Head",
            "sla": "4 hours",
            "actions": ["Priority queue assignment", "Supervisor review", "Customer update within 4 hours"]
        },
        "MEDIUM": {
            "team": "Senior Customer Support",
            "sla": "24 hours",
            "actions": ["Assigned to specialist", "Resolution within 24 hours"]
        },
        "LOW": {
            "team": "Auto-resolved / L1 Support",
            "sla": "48 hours",
            "actions": ["Standard resolution process", "Self-service options provided"]
        }
    }
}


def get_all_policies():
    """Returns a consolidated dictionary of all banking policies."""
    return {
        "transaction": TRANSACTION_POLICIES,
        "fraud": FRAUD_POLICIES,
        "card": CARD_POLICIES,
        "loan": LOAN_POLICIES,
        "general": GENERAL_POLICIES
    }


def get_policy_text_for_category(category: str) -> str:
    """Returns a formatted text block of all policies for a given category."""
    all_policies = get_all_policies()
    policies = all_policies.get(category, {})
    if not policies:
        return f"No specific policies found for category: {category}"
    
    text_parts = []
    for key, policy in policies.items():
        text_parts.append(f"\n### {policy['title']} ({policy['policy_id']})")
        text_parts.append(f"Auto-Resolution: {'Yes' if policy.get('auto_resolution') else 'No'}")
        text_parts.append(f"SLA: {policy.get('sla_hours', 'N/A')} hours")
        for i, rule in enumerate(policy['rules'], 1):
            text_parts.append(f"  {i}. {rule}")
    
    return "\n".join(text_parts)


def get_escalation_info(risk_level: str) -> dict:
    """Returns escalation details for a given risk level."""
    return ESCALATION_RULES["escalation_matrix"].get(
        risk_level.upper(), 
        ESCALATION_RULES["escalation_matrix"]["LOW"]
    )
