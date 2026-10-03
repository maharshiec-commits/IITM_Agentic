"""
Hierarchical, reactive, and hybrid planning.

Deck coverage:
- Hierarchical planning for stable, long-term workflows
- Reactive planning for fast-changing environments
- Hybrid agents that combine strategy with real-time adaptation
"""

from dataclasses import dataclass


@dataclass
class EnvironmentSignal:
    name: str
    severity: int
    description: str


class HierarchicalPlanner:
    """Top-down planner that decomposes a large goal into ordered subtasks."""

    def plan_trip_to_italy(self) -> list[str]:
        return [
            "Book international flights",
            "Reserve hotels in Rome, Florence, and Venice",
            "Create daily itinerary",
            "Purchase museum tickets",
            "Confirm train transfers",
        ]


class ReactivePlanner:
    """Real-time planner that responds to immediate environmental signals."""

    def respond(self, signal: EnvironmentSignal) -> str:
        if signal.name == "smoke_detected":
            return "Block hallway and prevent spread"
        if signal.name == "person_trapped":
            return "Switch priority to rescue operation"
        if signal.name == "route_blocked":
            return "Reroute using nearest safe path"
        if signal.severity >= 8:
            return "Escalate and request human intervention"
        return "Continue monitoring and adjust locally"


class HybridTravelAgent:
    """Uses a long-term itinerary but adapts when conditions change."""

    def __init__(self) -> None:
        self.base_plan = HierarchicalPlanner().plan_trip_to_italy()
        self.reactive_planner = ReactivePlanner()

    def update_plan(self, signals: list[EnvironmentSignal]) -> list[str]:
        updated_plan = list(self.base_plan)

        for signal in signals:
            if signal.name == "train_cancelled":
                updated_plan.append("Find alternate transport from Rome to Florence")
            elif signal.name == "weather_alert":
                updated_plan.append("Move outdoor activity to backup indoor museum")
            else:
                updated_plan.append(self.reactive_planner.respond(signal))

        return updated_plan


def main() -> None:
    print("Hierarchical plan:")
    for step in HierarchicalPlanner().plan_trip_to_italy():
        print(f"- {step}")

    print("\nReactive response:")
    signal = EnvironmentSignal("person_trapped", 10, "Fire team receives a life-safety alert")
    print(ReactivePlanner().respond(signal))

    print("\nHybrid plan update:")
    disruptions = [
        EnvironmentSignal("train_cancelled", 7, "Train to Florence cancelled"),
        EnvironmentSignal("weather_alert", 5, "Heavy rain forecast"),
    ]
    for step in HybridTravelAgent().update_plan(disruptions):
        print(f"- {step}")


if __name__ == "__main__":
    main()

