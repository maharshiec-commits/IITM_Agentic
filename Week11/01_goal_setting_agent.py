"""
Goal-setting in autonomous agents.

Deck coverage:
- Human-defined, system-generated, and adaptive goals
- Goal execution pipeline:
  interpretation -> decomposition -> planning -> execution -> reflection
- Healthcare triage example with governance and success metrics
"""

from dataclasses import dataclass, field
from typing import Callable


@dataclass
class PatientCase:
    name: str
    symptoms: list[str]
    vitals: dict[str, float]
    history_available: bool = True


@dataclass
class Goal:
    description: str
    success_criteria: list[str]
    constraints: list[str]
    subtasks: list[str] = field(default_factory=list)


@dataclass
class AgentDecision:
    priority: str
    rationale: list[str]
    actions: list[str]
    human_review_required: bool


class TriageAgent:
    """A compact example of a goal-oriented autonomous agent."""

    def __init__(self) -> None:
        self.audit_log: list[str] = []

    def interpret(self, case: PatientCase) -> Goal:
        self.audit_log.append(f"Interpreting patient case for {case.name}")
        return Goal(
            description="Assess medical urgency and recommend triage priority",
            success_criteria=[
                "recommendation generated quickly",
                "critical cases escalated immediately",
                "human clinician retains final authority",
            ],
            constraints=[
                "do not use demographics for priority scoring",
                "log reasoning for auditability",
                "escalate if life-threatening signals appear",
            ],
        )

    def decompose(self, goal: Goal) -> Goal:
        goal.subtasks = [
            "retrieve patient history",
            "collect current vitals",
            "analyse reported symptoms",
            "compare against severity rules",
            "generate recommendation",
        ]
        self.audit_log.append("Goal decomposed into triage subtasks")
        return goal

    def plan(self, goal: Goal, case: PatientCase) -> list[Callable[[], str]]:
        steps: list[Callable[[], str]] = []

        if case.history_available:
            steps.append(lambda: "History retrieved")
        else:
            steps.append(lambda: "History unavailable; using intake and live vitals")

        steps.extend(
            [
                lambda: f"Vitals collected: {case.vitals}",
                lambda: f"Symptoms analysed: {', '.join(case.symptoms)}",
                lambda: "Severity rules checked",
            ]
        )
        self.audit_log.append("Execution plan created")
        return steps

    def execute(self, case: PatientCase, steps: list[Callable[[], str]]) -> AgentDecision:
        results = [step() for step in steps]
        self.audit_log.extend(results)

        heart_rate = case.vitals.get("heart_rate", 0)
        oxygen = case.vitals.get("oxygen", 100)
        systolic_bp = case.vitals.get("systolic_bp", 120)
        symptoms = {symptom.lower() for symptom in case.symptoms}

        rationale: list[str] = []

        if oxygen < 90:
            rationale.append("oxygen saturation below critical threshold")
        if heart_rate > 130:
            rationale.append("heart rate indicates possible severe distress")
        if systolic_bp < 90:
            rationale.append("blood pressure indicates possible shock")
        if {"chest pain", "shortness of breath"} & symptoms:
            rationale.append("high-risk symptom pattern detected")

        if rationale:
            priority = "Critical"
            actions = ["activate emergency override", "alert clinician", "prepare critical care bay"]
        elif "fever" in symptoms or "severe pain" in symptoms:
            priority = "Urgent"
            rationale.append("symptoms require timely clinical assessment")
            actions = ["place patient in urgent queue", "notify triage nurse"]
        else:
            priority = "Routine"
            rationale.append("no immediate high-risk signals detected")
            actions = ["schedule standard assessment"]

        return AgentDecision(
            priority=priority,
            rationale=rationale,
            actions=actions,
            human_review_required=True,
        )

    def reflect(self, goal: Goal, decision: AgentDecision) -> str:
        if decision.human_review_required and decision.rationale:
            status = "success"
        else:
            status = "needs_review"

        self.audit_log.append(f"Reflection status: {status}")
        return (
            f"Goal: {goal.description}\n"
            f"Priority: {decision.priority}\n"
            f"Rationale: {decision.rationale}\n"
            f"Actions: {decision.actions}\n"
            f"Governance: clinician review required = {decision.human_review_required}\n"
            f"Reflection: {status}"
        )

    def run(self, case: PatientCase) -> str:
        goal = self.interpret(case)
        goal = self.decompose(goal)
        plan = self.plan(goal, case)
        decision = self.execute(case, plan)
        return self.reflect(goal, decision)


def main() -> None:
    case = PatientCase(
        name="Asha",
        symptoms=["shortness of breath", "dizziness"],
        vitals={"heart_rate": 142, "oxygen": 87, "systolic_bp": 88},
        history_available=False,
    )

    agent = TriageAgent()
    print(agent.run(case))
    print("\nAudit trail:")
    for entry in agent.audit_log:
        print(f"- {entry}")


if __name__ == "__main__":
    main()

