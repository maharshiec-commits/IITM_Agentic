# Runbook (Weeks 1–5)

## 1) Setup
```bash
python -m venv .venv
# Windows:
#   .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## 2) Run tests
```bash
pytest -q
```

## 3) Run the agent (one-shot)
```bash
python scripts/run_agent.py --text "VPN not connecting. Authentication failed." --user_id demo_user
```

## 4) Run the agent (interactive Q/A mode)
```bash
python scripts/run_agent.py --text "VPN not working" --interactive --user_id demo_user
```

## 5) Replay the canonical demo cases (VPN, Security, Admin Access)
```bash
python scripts/replay_conversations.py --cases tests/replay_cases.json --user_id demo_user
```

## 6) Logs and Metrics
After you run the agent, logs are written to:
- `logs/runs.jsonl` (audit trace: case + tool calls + final response)
- `logs/metrics.jsonl` (latency per tool + total latency + decision)

> Note: logs are ignored by git. The `logs/` folder is kept using `.gitkeep`.

## 7) Memory
Week 5 adds SQLite memory at:
- `data/memory.db` (created at runtime; ignored by git)

Run twice with same user to see reduced repeated questions:
```bash
python scripts/run_agent.py --text "VPN not connecting. Authentication failed." --user_id wajahat
python scripts/run_agent.py --text "VPN not connecting. Authentication failed." --interactive --user_id wajahat
```

## 8) Config
Default config: `config/default.yaml`
```bash
python scripts/run_agent.py --text "Need admin access to install Docker." --user_id demo_user --config config/default.yaml
```
