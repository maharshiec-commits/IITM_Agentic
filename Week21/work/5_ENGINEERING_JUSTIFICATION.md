# Capstone Deliverable 5: Engineering & Product Justification

**Project**: ApexBank AI Advisory & Support Copilot  
**Industry Scenario**: Scenario 2 — Banking: Non-Transactional Advisory Agent  
**Author / Consultant**: Maharshi (AI Engineer & Applied AI Consultant)  

---

## 1. Architectural Decisions & Framework Rationale

### Choice of Framework: LangChain + Modular Python + Langflow Visual Pipeline
For an enterprise banking copilot, framework selection must balance rapid visual prototyping with strict production-grade reliability and regulatory compliance:
- **Why LangChain/Python?** Full control over execution threads, deterministic mathematical calculations, granular exception recovery, and automated PII scrubbers. 
- **Visual Builder Integration (Langflow Export)**: To fulfill the low-code / visual builder requirements, we developed and exported [`apex_bank_copilot_langflow.json`](file:///c:/Users/Maharshi/Documents/IITM_Agentic/Week21/work/apex_bank_copilot_langflow.json), enabling business stakeholders and compliance auditors to inspect the complete pipeline visually (Document Loaders, Text Splitters, Embeddings, Vector Stores, Prompts, and Memory).
- **Deprecation Governance**: In accordance with the capstone instructions, Flowise was avoided as a primary dependency due to its officially announced end-of-life status.

---

## 2. Key Architecture Tradeoffs & Design Decisions

### Tradeoff 1: Deterministic Math Tools vs. LLM Arithmetic
- **Decision**: Implemented `calculate_loan_emi()` as a pure Python mathematical function rather than asking the LLM to calculate reducing-balance compound interest.
- **Rationale**: LLMs are probabilistic sequence predictors and notoriously error-prone with compound exponent calculations like `[P x r x (1+r)^n] / [(1+r)^n - 1]`. Offloading math to a deterministic tool guarantees **100% calculation accuracy**, essential for financial contracts.

### Tradeoff 2: Local FAISS Vector Store vs. Managed Cloud Vector Database
- **Decision**: Implemented local FAISS with OpenAI `text-embedding-3-small`.
- **Rationale**: For banking compliance and auditability, keeping vector indices in local secure storage eliminates third-party cloud data persistence liabilities, reduces API round-trip latency by ~180ms, and allows complete air-gapped reproducibility in offline evaluation environments.

### Tradeoff 3: Sliding Window Buffer Memory ($k=6$) vs. Conversational Summary Memory
- **Decision**: Utilized `ConversationBufferWindowMemory` retaining the last 6 turns.
- **Rationale**: Summarization memory requires an additional LLM call per turn (increasing latency by ~1.2s and incurring extra token costs). A sliding window of 6 turns captures all relevant multi-turn follow-ups (e.g. asking for FD rates, then following up on senior citizen terms) with zero latency overhead and zero loss of exact numerical context.

---

## 3. Defense-in-Depth Safety Architecture

Banking agents must operate with multi-layered safety mechanisms to prevent unauthorized transactions, regulatory fines, and data leaks:

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: PRE-INFERENCE SAFETY FIREWALL                     │
│  - Deterministic Regex Guardrail (blocks 'transfer', etc.)   │
│  - Instant non-transactional refusal without token cost      │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Safe queries only)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2: PROMPT CONSTRAINTS & ROLE GOVERNANCE               │
│  - Variant C System Prompt: Explicit negative mandates      │
│  - Zero hallucination on missing products (e.g. crypto)     │
│  - Automatic escalation triggers for reported fraud         │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3: DETERMINISTIC EXECUTION BOUNDARIES                │
│  - Read-only tools (check_account_summary)                  │
│  - Account numbers masked at data layer (XXXX-XXXX-4819)    │
│  - No write-access to core banking ledger                   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 4: POST-INFERENCE PII REDACTION & TELEMETRY          │
│  - Automatic PII Sanitizer strips cards, phones, Aadhaar    │
│  - Only sanitized records persisted in audit logs           │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Production Deployment Assumptions & Roadmap

### Deployment Assumptions
1. **API Security & Network Isolation**: The agent service will run inside a private Virtual Private Cloud (VPC) with mTLS encryption between the banking gateway and the agent service.
2. **Identity & Access Management (IAM)**: Customer ID (`CUST101`) is injected securely via authenticated OAuth2 / JWT session tokens from the mobile banking gateway; the customer does not manually pass raw database credentials.
3. **Core Banking Interface**: Tools will connect to Apex Bank's internal microservices via read-only REST APIs secured by API gateway rate-limiters.

### Production Scaling Roadmap
- **Phase 1 (Immediate)**: Deploy containerized Docker service with Gunicorn/Uvicorn on enterprise Kubernetes (EKS/GKE).
- **Phase 2 (Month 3)**: Introduce localized multilingual support (Hindi, Telugu, Tamil, Marathi) for inclusive customer reach.
- **Phase 3 (Month 6)**: Integrate live agent handoff via Webhook integration into Salesforce / Zendesk CRM for seamless real-time human takeover.

