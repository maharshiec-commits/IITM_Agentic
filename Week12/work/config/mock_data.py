"""
================================================================================
MOCK CUSTOMER & TRANSACTION DATA
================================================================================
Simulated customer records, transaction history, and account data.
Used by agents to look up customer context during query resolution.
================================================================================
"""

import random
from datetime import datetime, timedelta

# ──────────────────────────────────────────────────────────────────────────────
# MOCK CUSTOMER DATABASE
# ──────────────────────────────────────────────────────────────────────────────
CUSTOMER_DATABASE = {
    "CUST001": {
        "name": "Rajesh Kumar",
        "account_number": "XXXX-XXXX-4521",
        "account_type": "Savings",
        "segment": "Premium",
        "card_number": "XXXX-XXXX-XXXX-7890",
        "card_type": "Platinum Credit Card",
        "avg_monthly_spend": 45000,
        "international_enabled": True,
        "pending_loan": {"type": "Home Loan", "outstanding": 2500000, "emi": 28000, "months_remaining": 96},
        "recent_complaints": 0,
        "kyc_status": "Verified",
        "phone": "+91-98765-43210"
    },
    "CUST002": {
        "name": "Priya Sharma",
        "account_number": "XXXX-XXXX-8834",
        "account_type": "Savings",
        "segment": "Regular",
        "card_number": "XXXX-XXXX-XXXX-3456",
        "card_type": "Classic Debit Card",
        "avg_monthly_spend": 15000,
        "international_enabled": False,
        "pending_loan": None,
        "recent_complaints": 2,
        "kyc_status": "Verified",
        "phone": "+91-87654-32109"
    },
    "CUST003": {
        "name": "Amit Patel",
        "account_number": "XXXX-XXXX-2267",
        "account_type": "Current",
        "segment": "Business",
        "card_number": "XXXX-XXXX-XXXX-6789",
        "card_type": "Business Credit Card",
        "avg_monthly_spend": 250000,
        "international_enabled": True,
        "pending_loan": {"type": "Business Loan", "outstanding": 5000000, "emi": 85000, "months_remaining": 48},
        "recent_complaints": 1,
        "kyc_status": "Verified",
        "phone": "+91-99887-76655"
    },
    "CUST004": {
        "name": "Sneha Reddy",
        "account_number": "XXXX-XXXX-5590",
        "account_type": "Savings",
        "segment": "Regular",
        "card_number": "XXXX-XXXX-XXXX-1234",
        "card_type": "Gold Debit Card",
        "avg_monthly_spend": 22000,
        "international_enabled": False,
        "pending_loan": {"type": "Personal Loan", "outstanding": 300000, "emi": 12000, "months_remaining": 24},
        "recent_complaints": 0,
        "kyc_status": "Pending Update",
        "phone": "+91-77665-54433"
    }
}

# ──────────────────────────────────────────────────────────────────────────────
# MOCK RECENT TRANSACTIONS
# ──────────────────────────────────────────────────────────────────────────────
RECENT_TRANSACTIONS = {
    "CUST001": [
        {"txn_id": "TXN20260901001", "date": "2026-09-25", "amount": 4500, "merchant": "Amazon India", "type": "Online", "status": "Success", "location": "Mumbai"},
        {"txn_id": "TXN20260901002", "date": "2026-09-25", "amount": 4500, "merchant": "Amazon India", "type": "Online", "status": "Success", "location": "Mumbai"},
        {"txn_id": "TXN20260901003", "date": "2026-09-24", "amount": 85000, "merchant": "Dubai Mall", "type": "International POS", "status": "Success", "location": "Dubai, UAE"},
        {"txn_id": "TXN20260901004", "date": "2026-09-23", "amount": 2300, "merchant": "Swiggy", "type": "Online", "status": "Success", "location": "Mumbai"},
    ],
    "CUST002": [
        {"txn_id": "TXN20260902001", "date": "2026-09-26", "amount": 15000, "merchant": "ATM-SBI-Pune", "type": "ATM Withdrawal", "status": "Failed", "location": "Pune"},
        {"txn_id": "TXN20260902002", "date": "2026-09-26", "amount": 15000, "merchant": "ATM-SBI-Pune", "type": "ATM Withdrawal", "status": "Failed", "location": "Pune"},
        {"txn_id": "TXN20260902003", "date": "2026-09-25", "amount": 3200, "merchant": "Flipkart", "type": "Online", "status": "Success", "location": "Pune"},
    ],
    "CUST003": [
        {"txn_id": "TXN20260903001", "date": "2026-09-26", "amount": 175000, "merchant": "Unknown-Vendor-XYZ", "type": "NEFT", "status": "Success", "location": "Delhi"},
        {"txn_id": "TXN20260903002", "date": "2026-09-26", "amount": 225000, "merchant": "Unknown-Vendor-ABC", "type": "RTGS", "status": "Success", "location": "Singapore"},
        {"txn_id": "TXN20260903003", "date": "2026-09-26", "amount": 150000, "merchant": "Wire-Transfer-Global", "type": "International Wire", "status": "Pending", "location": "London, UK"},
        {"txn_id": "TXN20260903004", "date": "2026-09-25", "amount": 45000, "merchant": "Supplier-Local-123", "type": "NEFT", "status": "Success", "location": "Mumbai"},
    ],
    "CUST004": [
        {"txn_id": "TXN20260904001", "date": "2026-09-20", "amount": 12000, "merchant": "EMI-Auto-Debit", "type": "Auto-Debit", "status": "Failed", "location": "Hyderabad"},
        {"txn_id": "TXN20260904002", "date": "2026-09-18", "amount": 5500, "merchant": "BigBasket", "type": "Online", "status": "Success", "location": "Hyderabad"},
    ]
}


# ──────────────────────────────────────────────────────────────────────────────
# SAMPLE USER QUERIES (Test Inputs)
# ──────────────────────────────────────────────────────────────────────────────
SAMPLE_QUERIES = [
    # Query 1: Duplicate transaction (routine)
    {
        "id": "Q1",
        "customer_id": "CUST001",
        "query": "I was charged twice for the same Amazon order of Rs 4,500 on September 25th. Please refund the duplicate charge.",
        "expected_category": "transaction",
        "expected_risk": "LOW"
    },
    # Query 2: Failed ATM withdrawal — money debited (routine)
    {
        "id": "Q2",
        "customer_id": "CUST002",
        "query": "I tried to withdraw Rs 15,000 from an SBI ATM yesterday but the cash was not dispensed. However, my account has been debited. This happened twice. Please help.",
        "expected_category": "transaction",
        "expected_risk": "MEDIUM"
    },
    # Query 3: Fraud — unauthorized transactions (ESCALATION)
    {
        "id": "Q3",
        "customer_id": "CUST003",
        "query": "I did NOT make these transactions! There are three large transfers totalling over 5 lakhs to unknown vendors from Delhi, Singapore and London in the last 24 hours. This is FRAUD! Block my account immediately!",
        "expected_category": "fraud",
        "expected_risk": "CRITICAL"
    },
    # Query 4: EMI bounce / loan query (medium)
    {
        "id": "Q4",
        "customer_id": "CUST004",
        "query": "My personal loan EMI of Rs 12,000 was not deducted on September 20th due to insufficient balance. I have now added funds. Will there be a late fee? Will it affect my CIBIL score?",
        "expected_category": "loan",
        "expected_risk": "MEDIUM"
    },
    # Query 5: Card block request (routine)
    {
        "id": "Q5",
        "customer_id": "CUST001",
        "query": "I lost my wallet yesterday. Please block my Platinum credit card ending in 7890 immediately and issue a replacement.",
        "expected_category": "card",
        "expected_risk": "LOW"
    },
    # Query 6: Phishing victim (ESCALATION)
    {
        "id": "Q6",
        "customer_id": "CUST002",
        "query": "Someone called me claiming to be from the bank and I accidentally shared my OTP. Now I see Rs 8,000 debited from my account to some unknown UPI ID. I think I've been scammed.",
        "expected_category": "fraud",
        "expected_risk": "CRITICAL"
    },
    # Query 7: General inquiry — account statement (routine)
    {
        "id": "Q7",
        "customer_id": "CUST004",
        "query": "I need my account statement for the last 3 months for visa application. How can I get it?",
        "expected_category": "general",
        "expected_risk": "LOW"
    },
    # Query 8: Loan foreclosure inquiry
    {
        "id": "Q8",
        "customer_id": "CUST004",
        "query": "I want to close my personal loan early. What are the foreclosure charges and process? My remaining amount is about 3 lakhs.",
        "expected_category": "loan",
        "expected_risk": "LOW"
    },
    # Query 9: Suspicious activity — edge case (ESCALATION)
    {
        "id": "Q9",
        "customer_id": "CUST003",
        "query": "I notice multiple login attempts on my net banking from different IP addresses. I received 5 OTP messages in the last 30 minutes that I did not request. Something is very wrong.",
        "expected_category": "fraud",
        "expected_risk": "CRITICAL"
    },
    # Query 10: International transaction declined (routine)
    {
        "id": "Q10",
        "customer_id": "CUST002",
        "query": "I'm trying to make a purchase on an international website but my debit card keeps getting declined. What should I do?",
        "expected_category": "card",
        "expected_risk": "LOW"
    }
]


def get_customer_context(customer_id: str) -> str:
    """Returns a formatted summary of customer data for agent context."""
    customer = CUSTOMER_DATABASE.get(customer_id)
    if not customer:
        return f"Customer {customer_id} not found in the system."
    
    txns = RECENT_TRANSACTIONS.get(customer_id, [])
    
    context_parts = [
        f"=== Customer Profile ===",
        f"Name: {customer['name']}",
        f"Account: {customer['account_number']} ({customer['account_type']})",
        f"Segment: {customer['segment']}",
        f"Card: {customer['card_type']} ({customer['card_number']})",
        f"Avg Monthly Spend: INR {customer['avg_monthly_spend']:,}",
        f"International Transactions: {'Enabled' if customer['international_enabled'] else 'Disabled'}",
        f"KYC Status: {customer['kyc_status']}",
        f"Recent Complaints: {customer['recent_complaints']}",
    ]
    
    if customer.get('pending_loan'):
        loan = customer['pending_loan']
        context_parts.append(f"Active Loan: {loan['type']} | Outstanding: INR {loan['outstanding']:,} | EMI: INR {loan['emi']:,} | Remaining: {loan['months_remaining']} months")
    
    context_parts.append(f"\n=== Recent Transactions ===")
    for txn in txns:
        context_parts.append(
            f"  [{txn['date']}] {txn['txn_id']} | INR {txn['amount']:,} | {txn['merchant']} | {txn['type']} | {txn['status']} | {txn['location']}"
        )
    
    return "\n".join(context_parts)
