"""Quick import and compilation verification for the entire project."""
import sys
sys.path.insert(0, '.')

from config.policies import get_all_policies, get_policy_text_for_category, get_escalation_info
from config.mock_data import SAMPLE_QUERIES, CUSTOMER_DATABASE, get_customer_context
from agents import create_all_agents
from tasks import create_all_tasks

print("All imports OK")
print(f"Policies: {list(get_all_policies().keys())}")
print(f"Customers: {list(CUSTOMER_DATABASE.keys())}")
print(f"Sample queries: {len(SAMPLE_QUERIES)}")

esc = get_escalation_info("CRITICAL")
print(f"Escalation CRITICAL: {esc}")

ctx = get_customer_context("CUST001")
print(f"Customer context (CUST001): {ctx[:120]}...")

policy_txt = get_policy_text_for_category("fraud")
print(f"Fraud policy text (first 150 chars): {policy_txt[:150]}...")

print("\nAll verifications PASSED!")

