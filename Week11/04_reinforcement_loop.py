"""
Reinforcement loops in AI planning.

Deck coverage:
- Act -> observe -> adapt
- Learning through experience
- Static plans versus living processes
- Continuous improvement through measurable feedback
"""

from dataclasses import dataclass
from random import Random


@dataclass
class RouteChoice:
    route: str
    estimated_minutes: int


class NavigationAgent:
    """Learns which route works best from feedback over repeated trips."""

    def __init__(self, seed: int = 7) -> None:
        self.rng = Random(seed)
        self.route_scores = {
            "highway": 0.0,
            "city": 0.0,
            "scenic": 0.0,
        }
        self.exploration_rate = 0.30

    def act(self) -> RouteChoice:
        explore = self.rng.random() < self.exploration_rate
        if explore:
            route = self.rng.choice(list(self.route_scores))
        else:
            route = max(self.route_scores, key=self.route_scores.get)

        estimates = {
            "highway": 35,
            "city": 42,
            "scenic": 50,
        }
        return RouteChoice(route=route, estimated_minutes=estimates[route])

    def observe(self, choice: RouteChoice) -> int:
        traffic_penalty = {
            "highway": self.rng.choice([0, 5, 20]),
            "city": self.rng.choice([2, 4, 6]),
            "scenic": self.rng.choice([0, 1, 3]),
        }
        actual_minutes = choice.estimated_minutes + traffic_penalty[choice.route]
        reward = 60 - actual_minutes
        return reward

    def adapt(self, route: str, reward: int) -> None:
        learning_rate = 0.25
        old_score = self.route_scores[route]
        self.route_scores[route] = old_score + learning_rate * (reward - old_score)
        self.exploration_rate = max(0.05, self.exploration_rate * 0.96)

    def run_episode(self, episode_number: int) -> str:
        choice = self.act()
        reward = self.observe(choice)
        self.adapt(choice.route, reward)
        return (
            f"Episode {episode_number}: route={choice.route}, "
            f"reward={reward}, scores={self.route_scores}"
        )


def main() -> None:
    agent = NavigationAgent()
    for episode in range(1, 16):
        print(agent.run_episode(episode))

    best_route = max(agent.route_scores, key=agent.route_scores.get)
    print(f"\nLearned best route: {best_route}")


if __name__ == "__main__":
    main()

