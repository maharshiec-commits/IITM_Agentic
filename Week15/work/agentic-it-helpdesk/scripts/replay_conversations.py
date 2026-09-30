from __future__ import annotations
import json, argparse
from src.agent.replay import replay_cases
from src.agent.config import load_config
from src.agent.logging import JsonlLogger

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=str, required=True)
    parser.add_argument("--user_id", type=str, default="user_demo")
    parser.add_argument("--config", type=str, default="config/default.yaml")
    args = parser.parse_args()

    cfg = load_config(args.config)
    logger = JsonlLogger(cfg.logging)

    with open(args.cases, "r", encoding="utf-8") as f:
        cases = json.load(f)

    outs = replay_cases(cases, user_id=args.user_id, logger=logger)
    for i, out in enumerate(outs, 1):
        print("\n" + "="*80)
        print(f"REPLAY CASE {i}")
        print("="*80)
        print(out)

if __name__ == "__main__":
    main()
