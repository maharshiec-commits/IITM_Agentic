REQUIRED_HEADERS = [
    "## 1) Decision:",
    "## 2) Key Findings",
    "## 3) Steps / Plan",
    "## 4) Policy / Safety",
    "## 5) Evidence Used",
    "## 6) Next Steps",
]
def validate_response_sections(response: str) -> None:
    missing = [h for h in REQUIRED_HEADERS if h not in response]
    if missing:
        raise ValueError(f"Missing required sections: {missing}")
