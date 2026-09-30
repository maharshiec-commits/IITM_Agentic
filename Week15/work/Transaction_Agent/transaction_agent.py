"""
Transaction Resolution Agent — End-to-end workflow demo (single .py file)

This is a modified version of the "Order Status Resolution Agent" notebook demo.
Change: Order ID -> Transaction ID, and workflow operations are adapted accordingly.

Workflow:
1) Receive a "message" (simulated email/inbox event)
2) Extract Transaction ID (deterministic regex extraction)
3) Query backend (mock transaction database)
4) Decide next action (status response, missing ID request, not-found handling)
5) Compose a customer update (deterministic template; optional LLM phrasing)
6) Log interaction to a CSV "audit trail" (CRM-style)

Run:
    python transaction_agent_demo.py

Optional:
    Set USE_LLM=True and export OPENAI_API_KEY to enable LLM-based phrasing.
"""

from __future__ import annotations

import csv
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


# -----------------------------
# Configuration
# -----------------------------
USE_LLM = False  # set True to use LLM for response phrasing (requires OPENAI_API_KEY)
LLM_MODEL = "gpt-4o-mini"
LOG_PATH = Path("crm_transaction_log.csv")


# -----------------------------
# Input object (simulated inbox)
# -----------------------------
@dataclass
class Message:
    from_addr: str
    subject: str
    body: str
    received_at: datetime


def sample_message() -> Message:
    return Message(
        from_addr="customer@example.com",
        subject="Transaction status request: TXN-104512",
        body=(
            "Hello team,\n"
            "I made a payment and want to confirm the status.\n"
            "Transaction ID: TXN-104512\n"
            "Please share status and reference details.\n"
            "Thanks!"
        ),
        received_at=datetime.now(timezone.utc),
    )


# -----------------------------
# Step 1: Extract Transaction ID
# -----------------------------
# Accept formats like: TXN-12345, TXN-104512 (4 to 10 digits)
TXN_ID_RE = re.compile(r"\bTXN-\d{4,10}\b", re.IGNORECASE)


def extract_transaction_id(text: str) -> Optional[str]:
    """
    Deterministically extracts a Transaction ID from text.
    Returns normalized uppercase ID (e.g., TXN-104512) or None.
    """
    m = TXN_ID_RE.search(text)
    if not m:
        return None
    return m.group(0).upper()


# -----------------------------
# Step 2: Mock backend "database"
# -----------------------------
MOCK_TXN_DB: Dict[str, Dict[str, Any]] = {
    "TXN-104512": {
        "status": "SUCCESS",
        "amount": 2499.00,
        "currency": "INR",
        "merchant": "ACME Electronics",
        "payment_method": "UPI",
        "created_at": "2026-03-29T06:30:00Z",
        "utr": "UTR1234567890",
        "settlement_eta": "2026-03-29T18:00:00Z",
    },
    "TXN-204800": {
        "status": "PENDING",
        "amount": 799.00,
        "currency": "INR",
        "merchant": "QuickGrocer",
        "payment_method": "CARD",
        "created_at": "2026-03-29T08:10:00Z",
        "utr": None,
        "settlement_eta": "2026-03-30T12:00:00Z",
    },
    "TXN-999999": {
        "status": "FAILED",
        "amount": 1499.00,
        "currency": "INR",
        "merchant": "StreamFlix",
        "payment_method": "NETBANKING",
        "created_at": "2026-03-28T18:05:00Z",
        "utr": None,
        "settlement_eta": None,
        "failure_reason": "Bank declined the transaction",
    },
}


def get_transaction_record(txn_id: str) -> Optional[Dict[str, Any]]:
    """
    Simulates a backend lookup for transaction status.
    """
    return MOCK_TXN_DB.get(txn_id)


# -----------------------------
# Step 3: Compose customer update
# -----------------------------
def _compose_template_reply(customer_email: str, txn_id: str, rec: Dict[str, Any]) -> str:
    status = rec.get("status", "UNKNOWN")
    amount = rec.get("amount")
    currency = rec.get("currency", "")
    merchant = rec.get("merchant", "the merchant")
    method = rec.get("payment_method", "N/A")
    created_at = rec.get("created_at", "N/A")
    utr = rec.get("utr")
    settlement_eta = rec.get("settlement_eta")
    failure_reason = rec.get("failure_reason")

    lines = []
    lines.append(f"Subject: Update on your transaction {txn_id}")
    lines.append("")
    lines.append(f"Hello,")
    lines.append("")
    lines.append(f"Thanks for reaching out. We checked your transaction **{txn_id}**.")
    lines.append(f"- Status: **{status}**")
    if amount is not None:
        lines.append(f"- Amount: **{currency} {amount:.2f}**")
    lines.append(f"- Merchant: **{merchant}**")
    lines.append(f"- Payment method: **{method}**")
    lines.append(f"- Initiated at: **{created_at}**")

    if status == "SUCCESS":
        if utr:
            lines.append(f"- Reference (UTR): **{utr}**")
        if settlement_eta:
            lines.append(f"- Settlement expected by: **{settlement_eta}**")
        lines.append("")
        lines.append("If you still don’t see the update reflected, please share a screenshot of your bank statement entry, and we’ll investigate further.")
    elif status == "PENDING":
        if settlement_eta:
            lines.append(f"- Expected completion by: **{settlement_eta}**")
        lines.append("")
        lines.append("Pending transactions typically complete within the expected window. If it remains pending beyond that, we can raise an investigation.")
    elif status == "FAILED":
        if failure_reason:
            lines.append(f"- Reason (if available): **{failure_reason}**")
        lines.append("")
        lines.append("If the amount was debited, it is usually reversed automatically within your bank’s reversal window. If not reversed in time, we can help raise a dispute.")
    else:
        lines.append("")
        lines.append("We could not determine a definitive status from our systems. Please confirm the Transaction ID and try again.")

    lines.append("")
    lines.append("Regards,")
    lines.append("Support Team")
    return "\n".join(lines)


def _compose_llm_reply(customer_email: str, txn_id: str, rec: Dict[str, Any]) -> str:
    """
    Optional LLM phrasing: uses the transaction record as grounded facts,
    and asks the LLM to write a concise customer reply.
    """
    # Lazy import so the file runs without langchain dependencies by default.
    from langchain_openai import ChatOpenAI  # type: ignore

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set but USE_LLM=True")

    llm = ChatOpenAI(model=LLM_MODEL, temperature=0, api_key=api_key)

    prompt = f"""
You are a payment support assistant. Write a concise, polite update email (<=120 words).
Use ONLY the following transaction record facts (do not invent anything).

Customer email: {customer_email}
Transaction ID: {txn_id}
Transaction record (JSON-like):
{rec}

The email must:
- clearly state status and key next step
- avoid requesting unnecessary personal data
- include a short sign-off
""".strip()

    msg = llm.invoke(prompt)
    return msg.content if hasattr(msg, "content") else str(msg)


def compose_reply(customer_email: str, txn_id: str, rec: Dict[str, Any]) -> str:
    if USE_LLM:
        try:
            return _compose_llm_reply(customer_email, txn_id, rec)
        except Exception:
            # Fallback to deterministic template if LLM fails
            return _compose_template_reply(customer_email, txn_id, rec)
    return _compose_template_reply(customer_email, txn_id, rec)


# -----------------------------
# Step 4: CRM/Audit logging
# -----------------------------
def ensure_log_header(path: Path) -> None:
    if path.exists():
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            ["timestamp_utc", "from_addr", "subject", "transaction_id", "outcome", "notes"]
        )


def log_interaction(msg: Message, txn_id: Optional[str], outcome: str, notes: str) -> None:
    ensure_log_header(LOG_PATH)
    with LOG_PATH.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                datetime.now(timezone.utc).isoformat(),
                msg.from_addr,
                msg.subject,
                txn_id or "",
                outcome,
                notes[:500],
            ]
        )


# -----------------------------
# Orchestration (the agent brain)
# -----------------------------
@dataclass
class AgentResult:
    transaction_id: Optional[str]
    record_found: bool
    reply: str
    outcome: str


def handle_message(msg: Message) -> AgentResult:
    t0 = datetime.now(timezone.utc)

    combined_text = f"{msg.subject}\n{msg.body}"
    txn_id = extract_transaction_id(combined_text)

    if not txn_id:
        reply = (
            "Subject: Transaction ID required\n\n"
            "Hello,\n\n"
            "Thanks for reaching out. Could you please share your Transaction ID in the format TXN-12345? "
            "Once we have it, we’ll check the status and update you.\n\n"
            "Regards,\nSupport Team"
        )
        log_interaction(msg, None, "MISSING_TRANSACTION_ID", "No TXN-* identifier found in message")
        return AgentResult(None, False, reply, "MISSING_TRANSACTION_ID")

    rec = get_transaction_record(txn_id)
    if rec is None:
        reply = (
            f"Subject: Unable to locate transaction {txn_id}\n\n"
            "Hello,\n\n"
            f"We could not locate transaction **{txn_id}** in our system. "
            "Please double-check the Transaction ID and resend it. If you have multiple IDs, share the one shown in your bank/app history.\n\n"
            "Regards,\nSupport Team"
        )
        log_interaction(msg, txn_id, "TRANSACTION_NOT_FOUND", "No record found in backend")
        return AgentResult(txn_id, False, reply, "TRANSACTION_NOT_FOUND")

    reply = compose_reply(msg.from_addr, txn_id, rec)
    notes = f"Status={rec.get('status')} | Merchant={rec.get('merchant')} | Amount={rec.get('currency')} {rec.get('amount')}"
    log_interaction(msg, txn_id, "TRANSACTION_STATUS_SENT", notes)

    dt_ms = int((datetime.now(timezone.utc) - t0).total_seconds() * 1000)
    # include latency in notes in the log-friendly string
    log_interaction(msg, txn_id, "LATENCY", f"handle_message latency_ms={dt_ms}")

    return AgentResult(txn_id, True, reply, "TRANSACTION_STATUS_SENT")


# -----------------------------
# Demo runner
# -----------------------------
def main() -> None:
    msg = sample_message()
    print("=== Incoming Message ===")
    print(f"From: {msg.from_addr}")
    print(f"Subject: {msg.subject}")
    print(f"Received: {msg.received_at.isoformat()}")
    print("\nBody:\n" + msg.body)

    print("\n=== Agent Running Workflow ===")
    result = handle_message(msg)

    print("\n=== Extracted Transaction ID ===")
    print(result.transaction_id)

    print("\n=== Backend Record Found ===")
    print(result.record_found)

    print("\n=== Reply Generated ===")
    print(result.reply)

    print("\n=== Outcome ===")
    print(result.outcome)

    print(f"\n=== CRM Log Updated ===\n{LOG_PATH.resolve()}")


if __name__ == "__main__":
    main()