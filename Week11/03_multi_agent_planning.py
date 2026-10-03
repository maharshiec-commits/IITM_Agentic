"""
Multi-agent planning strategies.

Deck coverage:
- Centralised planning
- Decentralised planning
- Cooperative planning
- Competitive/mixed planning
- Communication, goal alignment, and conflict resolution
"""

from dataclasses import dataclass


@dataclass
class Agent:
    name: str
    role: str
    capacity: int


@dataclass
class Task:
    name: str
    effort: int
    priority: int


class CentralisedCoordinator:
    """One coordinator assigns work to all agents."""

    def assign(self, agents: list[Agent], tasks: list[Task]) -> dict[str, list[str]]:
        assignments = {agent.name: [] for agent in agents}
        remaining_capacity = {agent.name: agent.capacity for agent in agents}

        for task in sorted(tasks, key=lambda item: item.priority, reverse=True):
            available = [
                agent for agent in agents if remaining_capacity[agent.name] >= task.effort
            ]
            if not available:
                continue
            chosen = max(available, key=lambda agent: remaining_capacity[agent.name])
            assignments[chosen.name].append(task.name)
            remaining_capacity[chosen.name] -= task.effort

        return assignments


class DecentralisedCoordinator:
    """Agents choose tasks locally based on role fit and capacity."""

    def assign(self, agents: list[Agent], tasks: list[Task]) -> dict[str, list[str]]:
        assignments = {agent.name: [] for agent in agents}

        for agent in agents:
            role_tasks = [
                task
                for task in tasks
                if agent.role.lower() in task.name.lower() and task.effort <= agent.capacity
            ]
            if role_tasks:
                chosen = max(role_tasks, key=lambda item: item.priority)
                assignments[agent.name].append(chosen.name)

        return assignments


class CooperativeKitchen:
    """Specialised agents collaborate toward a shared outcome."""

    def prepare_order(self) -> list[str]:
        return [
            "Chef plans dish timing",
            "Sous-chef prepares ingredients",
            "Line cook executes hot items",
            "Waitstaff coordinates delivery",
            "All agents share status updates until order is served",
        ]


class CompetitiveMarket:
    """Agents pursue individual goals while respecting shared system rules."""

    def trade(self, prices: list[float]) -> dict[str, str]:
        latest_price = prices[-1]
        average_price = sum(prices) / len(prices)

        return {
            "momentum_bot": "buy" if latest_price > average_price else "hold",
            "value_bot": "buy" if latest_price < average_price * 0.98 else "hold",
            "risk_guard": "allow" if abs(latest_price - average_price) < average_price * 0.1 else "block",
        }


def main() -> None:
    agents = [
        Agent("Drone-A", "pickup", 5),
        Agent("Robot-B", "sort", 4),
        Agent("Van-C", "delivery", 8),
    ]
    tasks = [
        Task("pickup medical package", 3, 9),
        Task("sort warehouse shelf", 2, 6),
        Task("delivery hospital route", 6, 10),
        Task("pickup backup battery", 4, 5),
    ]

    print("Centralised planning:")
    print(CentralisedCoordinator().assign(agents, tasks))

    print("\nDecentralised planning:")
    print(DecentralisedCoordinator().assign(agents, tasks))

    print("\nCooperative planning:")
    for step in CooperativeKitchen().prepare_order():
        print(f"- {step}")

    print("\nCompetitive/mixed planning:")
    print(CompetitiveMarket().trade([100.0, 101.0, 103.0, 102.5]))


if __name__ == "__main__":
    main()

