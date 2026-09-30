from __future__ import annotations
import argparse
from src.agent.agent import run_once, run_interactive
from src.agent.config import load_config
from src.agent.logging import JsonlLogger

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, required=True)
    parser.add_argument("--interactive", action="store_true")
    parser.add_argument("--config", type=str, default="config/default.yaml")
    parser.add_argument("--user_id", type=str, default="user_demo")
    parser.add_argument("--ticket_id", type=str, default=None)
    args = parser.parse_args()

    cfg = load_config(args.config)
    logger = JsonlLogger(cfg.logging)

    if args.interactive:
        run_interactive(args.text, user_id=args.user_id, ticket_id=args.ticket_id, logger=logger, config_path=args.config)
    else:
        _, response = run_once(args.text, user_id=args.user_id, ticket_id=args.ticket_id, logger=logger, config_path=args.config)
        print(response)
        print(f"\n[Logs] audit: {cfg.logging.dir}/{cfg.logging.audit_file}")
        print(f"[Logs] metrics: {cfg.logging.dir}/{cfg.logging.metrics_file}")

if __name__ == "__main__":
    main()
