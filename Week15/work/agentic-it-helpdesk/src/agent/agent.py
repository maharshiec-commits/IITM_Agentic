from __future__ import annotations
import uuid, re
from dataclasses import asdict
from typing import Any, Dict, List, Optional, Tuple

from src.models import TicketCase, ToolResult
from src.agent.formatters import format_response
from src.agent.validators import validate_response_sections
from src.agent.logging import JsonlLogger
from src.agent.metrics import RunMetrics, Timer
from src.agent.config import load_config
from src.tools.registry import run_tool_timed

from src.memory.store import MemoryStore, MemoryItem
from src.memory.selectors import select_relevant_user_memory, select_relevant_case_memory
from src.memory.summarizer import summarize_for_case_memory

def _new_case(user_id: str, ticket_text: str, ticket_id: Optional[str] = None, user_context: Optional[Dict[str, Any]] = None) -> TicketCase:
    return TicketCase(case_id=f"CASE-{uuid.uuid4().hex[:8]}", ticket_id=ticket_id, user_id=user_id, ticket_text=ticket_text, user_context=user_context or {})

def _log_tool(case: TicketCase, tr: ToolResult) -> None:
    case.audit_log.append({"tool": tr.tool, "status": tr.status, "confidence": tr.confidence, "data": tr.data, "audit": tr.audit, "error": tr.error})

def _policy_actions_from_plan(plan_steps: List[str], category: str) -> List[str]:
    actions: List[str] = []
    if category == "security":
        actions.append("security_incident")
    joined = " ".join(plan_steps).lower()
    if "password" in joined and ("reset" in joined or "change" in joined):
        actions.append("password_reset")
    if "admin" in joined or "elevation" in joined or "privileged" in joined:
        actions.append("grant_admin_access")
    if category == "vpn":
        actions.append("vpn_guided_fix")
    return sorted(set(actions))

def run_once(ticket_text: str, user_id: str = "user_demo", ticket_id: Optional[str] = None, user_context: Optional[Dict[str, Any]] = None,
             logger: Optional[JsonlLogger] = None, config_path: str = "config/default.yaml") -> Tuple[TicketCase, str]:
    cfg = load_config(config_path)
    logger = logger or JsonlLogger(cfg.logging)
    run_id = f"RUN-{uuid.uuid4().hex[:10]}"
    tool_metrics = []
    total_timer = Timer()

    case = _new_case(user_id, ticket_text, ticket_id, user_context)

    mem = MemoryStore()
    user_mem_all = mem.get_user_memory(user_id)
    case_mem_all = mem.get_case_memory(case.case_id)

    for k in ("os","device","preferred_language"):
        if k in user_mem_all and k not in case.user_context:
            case.user_context[k] = user_mem_all[k]
    case.user_context["case_memory"] = select_relevant_case_memory(case_mem_all)

    # classify
    tr, m = run_tool_timed("classify_ticket", ticket_text=case.ticket_text)
    tool_metrics.append(m); _log_tool(case, tr)
    case.classification = {**tr.data, "confidence": tr.confidence}
    category = case.classification.get("category", "other")

    # inject category-specific memory
    for k, v in select_relevant_user_memory(user_mem_all, category).items():
        if k not in case.user_context:
            case.user_context[k] = v

    # missing info
    if tr.confidence < cfg.agent.conf_threshold or category == "other":
        req, m2 = run_tool_timed("extract_requirements", category=category, ticket_text=case.ticket_text, known_context=case.user_context)
        tool_metrics.append(m2); _log_tool(case, req)
        case.missing_info = req.data

        decision = "request_more_info"
        response = format_response(case, decision, [], None, {"hitl_required": False}, None)
        validate_response_sections(response)

        summary = summarize_for_case_memory([], [], case.missing_info.get("questions", []), decision)
        mem.upsert_case_memory(case.case_id, "summary", summary)
        mem.upsert_case_memory(case.case_id, "last_decision", decision)

        metrics = RunMetrics(run_id=run_id, total_latency_ms=total_timer.stop_ms(), decision=decision, tool_metrics=tool_metrics)
        logger.log_case(run_id, case, response); logger.log_metrics(metrics)
        return case, response

    # kb search
    kb, m3 = run_tool_timed("kb_search", query=f"{category} {case.ticket_text}", top_k=cfg.agent.kb_top_k)
    tool_metrics.append(m3); _log_tool(case, kb)
    case.kb_results = kb.data.get("results", [])

    # plan
    plan, m4 = run_tool_timed("generate_resolution_plan", ticket_case=asdict(case), kb_results=case.kb_results)
    tool_metrics.append(m4); _log_tool(case, plan)
    case.plan = plan.data

    # policy gate
    actions = _policy_actions_from_plan(case.plan.get("steps", []), category)
    policy_decisions = []
    hitl_required = False
    escalation_target = None

    for action in actions:
        pc, m5 = run_tool_timed("policy_check", action=action, context={"category": category, **case.user_context})
        tool_metrics.append(m5); _log_tool(case, pc)
        policy_decisions.append({"action": action, **pc.data})
        if pc.data.get("decision") == "requires_approval":
            hitl_required = True
        if pc.data.get("decision") == "requires_escalation":
            escalation_target = "SecOps"

    case.policy = {"actions": actions, "decisions": policy_decisions, "hitl_required": hitl_required}

    # security escalation
    if cfg.policy.always_escalate_security and (category == "security" or escalation_target == "SecOps"):
        esc, m6 = run_tool_timed("create_escalation_note", ticket_case=asdict(case),
                                evidence={"what_tried": [], "recommended_next_action": "Start incident response triage with preserved evidence.",
                                          "risk_notes": ["User reported phishing/OTP event."]},
                                target_team="SecOps")
        tool_metrics.append(m6); _log_tool(case, esc)
        case.escalation = {"needed": True, "target_team": "SecOps", **esc.data}

        decision = "escalate_to_SecOps"
        response = format_response(case, decision, case.kb_results[:1], case.plan, {"hitl_required": True}, case.escalation)
        validate_response_sections(response)

        kb_ids = [r.get("kb_id") for r in case.kb_results[:1] if r.get("kb_id")]
        summary = summarize_for_case_memory(case.plan.get("steps", []), kb_ids, [], decision)
        mem.upsert_case_memory(case.case_id, "summary", summary)
        mem.upsert_case_memory(case.case_id, "last_decision", decision)

        metrics = RunMetrics(run_id=run_id, total_latency_ms=total_timer.stop_ms(), decision=decision, tool_metrics=tool_metrics)
        logger.log_case(run_id, case, response); logger.log_metrics(metrics)
        return case, response

    # approval required
    if hitl_required:
        decision = "requires_approval"
        response = format_response(case, decision, case.kb_results[:1], case.plan, {"hitl_required": True}, None)
        validate_response_sections(response)

        kb_ids = [r.get("kb_id") for r in case.kb_results[:1] if r.get("kb_id")]
        summary = summarize_for_case_memory(case.plan.get("steps", []), kb_ids, [], decision)
        mem.upsert_case_memory(case.case_id, "summary", summary)
        mem.upsert_case_memory(case.case_id, "last_decision", decision)

        metrics = RunMetrics(run_id=run_id, total_latency_ms=total_timer.stop_ms(), decision=decision, tool_metrics=tool_metrics)
        logger.log_case(run_id, case, response); logger.log_metrics(metrics)
        return case, response

    # normal resolve
    decision = "resolve_guidance"
    response = format_response(case, decision, case.kb_results[:1], case.plan, {"hitl_required": False}, None)
    validate_response_sections(response)

    # persist stable user memory
    if case.user_context.get("os"):
        mem.upsert_user_memory(user_id, MemoryItem("os", case.user_context["os"], 0.9))
    if case.user_context.get("device"):
        mem.upsert_user_memory(user_id, MemoryItem("device", case.user_context["device"], 0.9))

    kb_ids = [r.get("kb_id") for r in case.kb_results[:1] if r.get("kb_id")]
    summary = summarize_for_case_memory(case.plan.get("steps", []), kb_ids, [], decision)
    mem.upsert_case_memory(case.case_id, "summary", summary)
    mem.upsert_case_memory(case.case_id, "last_decision", decision)

    metrics = RunMetrics(run_id=run_id, total_latency_ms=total_timer.stop_ms(), decision=decision, tool_metrics=tool_metrics)
    logger.log_case(run_id, case, response); logger.log_metrics(metrics)
    return case, response

def run_interactive(ticket_text: str, user_id: str = "user_demo", ticket_id: Optional[str] = None, user_context: Optional[Dict[str, Any]] = None,
                    logger: Optional[JsonlLogger] = None, config_path: str = "config/default.yaml") -> None:
    cfg = load_config(config_path)
    logger = logger or JsonlLogger(cfg.logging)
    context = dict(user_context or {})
    current_text = ticket_text

    while True:
        case, response = run_once(current_text, user_id=user_id, ticket_id=ticket_id, user_context=context, logger=logger, config_path=config_path)
        print("\n" + response + "\n")

        if "Decision: request_more_info" in response:
            questions = case.missing_info.get("questions", [])
            if questions:
                print("Please answer these questions (one line each). Press Enter to skip.\n")
                for q in questions:
                    ans = input(q + " ")
                    if ans.strip():
                        key = re.sub(r"\W+", "_", q.lower()).strip("_")[:40]
                        context[key] = ans.strip()
            current_text = ticket_text + "\nAdditional context: " + " | ".join([str(v) for v in context.values()])
            continue

        if "Decision: requires_approval" in response or "Decision: escalate_to_SecOps" in response:
            ans = input("Approve the required approval/escalation step? (yes/no): ").strip().lower()
            if ans == "yes":
                print("Recorded approval. (Future weeks can trigger workflows; stopping safely now.)")
            else:
                print("Approval not granted. Stopping safely.")
            break
        break
