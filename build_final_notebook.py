"""
IITM Agentic AI — Beautiful Colorful Handwritten Notebook Generator
Covers ALL 21 Weeks of the Professional Certificate Programme
Generates a single gorgeous PDF via Edge Headless
"""
import os, sys, subprocess
from pathlib import Path

WORKSPACE = Path(r"C:\Users\Maharshi\Documents\IITM_Agentic")
HTML_OUT = WORKSPACE / "IITM_Final_Beautiful_Notebook.html"
PDF_OUT  = WORKSPACE / "IITM_Final_Beautiful_Notebook.pdf"
EDGE     = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>IITM Agentic AI — Master Notebook</title>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Kalam:wght@400;700&family=Fira+Code:wght@400;600&family=Patrick+Hand&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{
  background:#f0ebe0;
  font-family:'Patrick Hand','Caveat',cursive;
  font-size:16px; line-height:1.65; color:#1e293b;
  padding:20px;
}
.notebook{
  max-width:1100px; margin:0 auto;
  background:#fffef9;
  background-image:
    linear-gradient(90deg,rgba(220,38,38,.18) 0 2px,transparent 2px),
    linear-gradient(#dde4ef 1px,transparent 1px);
  background-size:68px 100%, 100% 34px;
  background-position:60px 0, 0 12px;
  border-radius:14px;
  box-shadow:0 8px 40px rgba(0,0,0,.18),4px 0 0 #f59e0b inset;
  padding:50px 60px 60px 90px;
  position:relative;
}
.notebook::before{
  content:'';position:absolute;top:50px;left:26px;bottom:50px;width:14px;
  background:radial-gradient(circle,#bbb 5px,transparent 6px);
  background-size:14px 110px;
}
/* Cover */
.cover{
  text-align:center;padding:40px 20px 50px;border-bottom:3px double #f59e0b;margin-bottom:40px;
}
.cover-badge{
  display:inline-block;padding:5px 18px;border-radius:20px;font-size:.85rem;font-weight:700;
  letter-spacing:.07em;text-transform:uppercase;
  background:#1e40af;color:#fff;margin-bottom:15px;
}
.cover h1{
  font-family:'Kalam',cursive;font-size:3rem;color:#0f172a;
  text-shadow:2px 2px 0 #fde68a;margin:10px 0;
}
.cover h2{font-size:1.5rem;color:#475569;font-weight:400;margin:8px 0;}
.cover p{font-size:1rem;color:#64748b;margin-top:14px;}
.meta-chips{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin-top:18px;}
.chip{padding:4px 12px;border-radius:999px;font-size:.78rem;font-weight:700;border:1.5px solid;}
.chip-blue{background:#eff6ff;color:#1d4ed8;border-color:#3b82f6;}
.chip-green{background:#f0fdf4;color:#065f46;border-color:#10b981;}
.chip-orange{background:#fff7ed;color:#c2410c;border-color:#f97316;}
.chip-purple{background:#faf5ff;color:#6b21a8;border-color:#a855f7;}
/* Week Card */
.week{
  margin:32px 0;border-radius:12px;overflow:hidden;
  box-shadow:0 4px 16px rgba(0,0,0,.07);border:1.5px solid #e2e8f0;
}
.week-header{
  padding:14px 20px;display:flex;align-items:center;gap:14px;
  font-family:'Kalam',cursive;font-size:1.3rem;font-weight:700;color:#fff;
}
.week-body{background:#fff;padding:18px 24px;}
/* Color themes per week group */
.w1{background:linear-gradient(135deg,#dc2626,#ef4444);}
.w2{background:linear-gradient(135deg,#d97706,#f59e0b);}
.w3{background:linear-gradient(135deg,#059669,#10b981);}
.w4{background:linear-gradient(135deg,#1d4ed8,#3b82f6);}
.w5{background:linear-gradient(135deg,#7c3aed,#8b5cf6);}
.w6{background:linear-gradient(135deg,#db2777,#ec4899);}
.w7{background:linear-gradient(135deg,#0369a1,#0ea5e9);}
.w8{background:linear-gradient(135deg,#b45309,#d97706);}
.w9{background:linear-gradient(135deg,#15803d,#22c55e);}
.w10{background:linear-gradient(135deg,#7e22ce,#a855f7);}
.w11{background:linear-gradient(135deg,#be123c,#f43f5e);}
.w12{background:linear-gradient(135deg,#0c4a6e,#0284c7);}
.w13{background:linear-gradient(135deg,#854d0e,#ca8a04);}
.w14{background:linear-gradient(135deg,#166534,#16a34a);}
.w15{background:linear-gradient(135deg,#1e3a8a,#4f46e5);}
.w16{background:linear-gradient(135deg,#9d174d,#db2777);}
.w17{background:linear-gradient(135deg,#7c3aed,#c026d3);}
.w18{background:linear-gradient(135deg,#dc2626,#b91c1c);}
.w19{background:linear-gradient(135deg,#0369a1,#0891b2);}
.w20{background:linear-gradient(135deg,#065f46,#0d9488);}
.w21{background:linear-gradient(135deg,#1e1b4b,#4338ca);}
.week-num{
  background:rgba(255,255,255,.25);border-radius:8px;
  padding:4px 10px;font-size:1rem;white-space:nowrap;
}
/* Content blocks inside week */
.summary{
  background:#f8fafc;border-left:5px solid #f59e0b;
  border-radius:0 8px 8px 0;padding:10px 16px;margin-bottom:14px;
  font-size:1.02rem;
}
.concepts{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;}
.concept{
  padding:10px 14px;border-radius:8px;font-size:.93rem;
  box-shadow:0 2px 6px rgba(0,0,0,.04);border:1px solid #e2e8f0;
}
.c-red{background:#fef2f2;border-left:4px solid #ef4444;}
.c-blue{background:#eff6ff;border-left:4px solid #3b82f6;}
.c-green{background:#f0fdf4;border-left:4px solid #10b981;}
.c-orange{background:#fff7ed;border-left:4px solid #f97316;}
.c-purple{background:#faf5ff;border-left:4px solid #a855f7;}
.c-pink{background:#fdf2f8;border-left:4px solid #ec4899;}
.concept strong{display:block;font-family:'Kalam',cursive;font-size:1rem;color:#0f172a;margin-bottom:4px;}
.tip{
  display:flex;gap:8px;align-items:flex-start;
  padding:8px 12px;border-radius:6px;background:#fffbeb;
  border:1px dashed #fbbf24;font-size:.88rem;margin-top:10px;
}
.tip .icon{font-size:1.2rem;flex-shrink:0;}
code{
  font-family:'Fira Code',monospace;font-size:.85em;
  background:#1e293b;color:#38bdf8;padding:2px 6px;border-radius:4px;
}
/* Section dividers */
h3.section{
  font-family:'Kalam',cursive;font-size:1.55rem;color:#0f172a;
  border-bottom:2px solid #fde68a;padding-bottom:6px;margin:38px 0 20px;
  display:flex;align-items:center;gap:10px;
}
/* Footer */
footer{
  text-align:center;margin-top:50px;padding:20px;
  border-top:2px dashed #cbd5e1;color:#64748b;font-size:.9rem;
}
@media print{
  body{background:#fff;padding:0;}
  .notebook{box-shadow:none;background-image:none;padding:20px 25px 25px 40px;}
  .notebook::before{display:none;}
  .week{break-inside:avoid;}
}
</style>
</head>
<body>
<div class="notebook">

<!-- COVER PAGE -->
<div class="cover">
  <div class="cover-badge">🏛️ IIT Madras Pravartak</div>
  <h1>Agentic AI & Applications</h1>
  <h2>Professional Certificate Programme — Master Notebook</h2>
  <p>Complete 21-Week Handwritten Study Notes · All Frameworks · All Concepts</p>
  <div class="meta-chips">
    <span class="chip chip-blue">Python · LangChain · CrewAI · AutoGen</span>
    <span class="chip chip-green">RAG · MCP · ReAct · RLHF</span>
    <span class="chip chip-orange">FastAPI · FAISS · LangSmith · LangFlow</span>
    <span class="chip chip-purple">Ethics · Safety · Governance · Capstone</span>
  </div>
</div>

<!-- ─── PART A: FOUNDATIONS (Weeks 1–6) ─── -->
<h3 class="section">🎨 PART A: Foundations of Python & AI (Weeks 1–6)</h3>

<div class="week">
  <div class="week-header w1"><span class="week-num">Week 1</span> Getting Started: Python & ChatGPT</div>
  <div class="week-body">
    <div class="summary">🔴 <strong>Core Idea:</strong> Python is the universal language of AI. ChatGPT is a transformer-based LLM that predicts the next token using attention weights over a context window—not by "thinking" like humans.</div>
    <div class="concepts">
      <div class="concept c-red"><strong>🐍 Python Basics</strong>Variables, data types, control flow, functions. Foundation of all AI scripting.</div>
      <div class="concept c-blue"><strong>💬 ChatGPT Mechanics</strong>Token prediction engine using causal attention. Temperature controls randomness.</div>
      <div class="concept c-green"><strong>⚡ Prompt Engineering Intro</strong>Prompt = input context. Better prompts = better completions. System vs User roles.</div>
      <div class="concept c-orange"><strong>🔄 API Basics</strong>OpenAI REST API: <code>chat.completions.create()</code>. JSON request → JSON response.</div>
    </div>
    <div class="tip"><span class="icon">💡</span>Java Parallel: Think of a ChatGPT call like invoking a microservice method—you send a JSON request, get a JSON response. The "model" is the remote service logic.</div>
  </div>
</div>

<div class="week">
  <div class="week-header w2"><span class="week-num">Week 2</span> Python: Data Types, Variables, Control Flow & Functions</div>
  <div class="week-body">
    <div class="summary">🟠 <strong>Core Idea:</strong> Python's duck typing and list comprehensions allow rapid AI data wrangling. Mastering closures and decorators enables writing clean tool functions for LangChain agents.</div>
    <div class="concepts">
      <div class="concept c-orange"><strong>📦 Data Structures</strong>Lists, dicts, sets, tuples. Dicts are king in AI for config, prompt templates, and tool schemas.</div>
      <div class="concept c-green"><strong>🔁 Control Flow</strong><code>for/while/if/try/except</code>. Exception handling is mandatory in production LLM calls.</div>
      <div class="concept c-blue"><strong>🎯 Functions & Decorators</strong><code>@tool</code> decorator in LangChain wraps any Python function into an agent-callable tool.</div>
      <div class="concept c-purple"><strong>🧩 Comprehensions</strong><code>[x for x in data if condition]</code> — Used everywhere in embedding pipelines and chunk filtering.</div>
    </div>
    <div class="tip"><span class="icon">💡</span>Java Parallel: Python dict = Java LinkedHashMap. Python list comprehension = Java Stream.filter().map().collect().</div>
  </div>
</div>

<div class="week">
  <div class="week-header w3"><span class="week-num">Week 3</span> Working with Libraries: NumPy, Pandas, Matplotlib</div>
  <div class="week-body">
    <div class="summary">🟢 <strong>Core Idea:</strong> NumPy provides the numerical backbone for vector math; Pandas handles tabular data pipelines; Matplotlib visualizes AI model behavior. Essential for debugging embeddings and similarity scores.</div>
    <div class="concepts">
      <div class="concept c-green"><strong>🔢 NumPy Arrays</strong>N-dimensional arrays with vectorized math. Embeddings ARE numpy float32 arrays of dimension 1536.</div>
      <div class="concept c-blue"><strong>🐼 Pandas DataFrame</strong>2D labelled data structure. Load CSV → DataFrame → feed agent. Like a Java ResultSet with superpowers.</div>
      <div class="concept c-orange"><strong>📊 Matplotlib</strong>Plot similarity distributions, loss curves, attention maps. Critical for model evaluation reports.</div>
      <div class="concept c-red"><strong>🔗 Integration</strong>Pandas + NumPy → compute cosine similarity between embedding batches efficiently.</div>
    </div>
    <div class="tip"><span class="icon">⚠️</span>Cosine Similarity Formula: <code>cos(θ) = A·B / (|A|×|B|)</code> — Values near 1.0 = very similar. Used in RAG retrieval ranking.</div>
  </div>
</div>

<div class="week">
  <div class="week-header w4"><span class="week-num">Week 4</span> Fundamentals of AI & Machine Learning</div>
  <div class="week-body">
    <div class="summary">🔵 <strong>Core Idea:</strong> AI = systems that learn patterns from data. ML distinguishes supervised (labelled training), unsupervised (clustering), and reinforcement (reward-based) paradigms—each underpinning different agentic capabilities.</div>
    <div class="concepts">
      <div class="concept c-blue"><strong>📚 Supervised Learning</strong>Input → Label. Train model on examples. Foundation of NLP classifiers and intent detection agents.</div>
      <div class="concept c-green"><strong>🌀 Unsupervised Learning</strong>Find hidden patterns. k-means, PCA. Used in clustering customer queries before routing to agents.</div>
      <div class="concept c-orange"><strong>🎮 Reinforcement Learning</strong>Agent + Environment + Reward. RLHF uses human feedback to fine-tune LLMs (GPT, Gemini).</div>
      <div class="concept c-purple"><strong>🧠 Neural Networks</strong>Layers of weighted activations. Transformers are deep multi-layer attention networks.</div>
      <div class="concept c-red"><strong>📈 Bias vs Variance</strong>Underfitting = too simple. Overfitting = memorized training data. Validation loss reveals both.</div>
      <div class="concept c-pink"><strong>🔄 Gradient Descent</strong>Iteratively adjust weights to minimize loss. Adam optimizer: adaptive gradient + momentum.</div>
    </div>
    <div class="tip"><span class="icon">💡</span>Java Parallel: A neural network is like a pipeline of Transformer lambdas—each layer transforms the input tensor to produce a more abstract representation.</div>
  </div>
</div>

<div class="week">
  <div class="week-header w5"><span class="week-num">Week 5</span> Large Language Models (LLMs) — Part 1 & 2</div>
  <div class="week-body">
    <div class="summary">🟣 <strong>Core Idea:</strong> Transformers use self-attention to weigh every token against every other token in the context window simultaneously. Temperature and top-p control output sampling—critical levers for determinism in production agents.</div>
    <div class="concepts">
      <div class="concept c-purple"><strong>⚡ Attention Mechanism</strong>Q·Kᵀ/√d_k → Softmax → ×V. Each token attends to all others. Context = extended working memory.</div>
      <div class="concept c-blue"><strong>🌡️ Temperature</strong>t=0.0: deterministic (best for tool calls). t=1.0: creative. t>1.2: chaotic. Production agents use t≤0.1.</div>
      <div class="concept c-red"><strong>🎛️ Top-p / Top-k Sampling</strong>Top-p=0.9: sample from top 90% probability mass. Reduces hallucinations in structured outputs.</div>
      <div class="concept c-green"><strong>📝 Tokenization (BPE)</strong>Byte-Pair Encoding merges frequent byte pairs into tokens. 1 token ≈ 4 chars in English.</div>
      <div class="concept c-orange"><strong>🪟 Context Window</strong>Maximum tokens (input+output). GPT-4o-mini: 128k tokens. Agents must budget context carefully.</div>
      <div class="concept c-pink"><strong>🔮 In-Context Learning</strong>LLMs "learn" tasks from examples in the prompt (zero/few-shot) without weight updates.</div>
    </div>
    <div class="tip"><span class="icon">🔴</span>Critical Production Rule: Always set <code>temperature=0.1</code> and <code>max_tokens=1500</code> for agent tool-calling nodes. Higher temperature causes hallucinated JSON schemas.</div>
  </div>
</div>

<div class="week">
  <div class="week-header w6"><span class="week-num">Week 6</span> Embedding Models & Vector Basics</div>
  <div class="week-body">
    <div class="summary">💗 <strong>Core Idea:</strong> Embeddings convert text into dense floating-point vectors that capture semantic meaning geometrically. Similar meanings → nearby vectors in high-dimensional space. This is the mathematical core of RAG systems.</div>
    <div class="concepts">
      <div class="concept c-pink"><strong>🧮 Embeddings</strong>text → float[1536]. OpenAI <code>text-embedding-3-small</code>: 1536-dim. Captures semantic context as coordinates.</div>
      <div class="concept c-blue"><strong>📐 Cosine Similarity</strong>Measures angle between vectors. Score 1.0 = identical meaning. Used to rank retrieved chunks in RAG.</div>
      <div class="concept c-green"><strong>🗄️ Vector Stores</strong>FAISS (Facebook AI Similarity Search): indexes millions of vectors for sub-millisecond kNN lookup.</div>
      <div class="concept c-orange"><strong>🔍 Semantic Search</strong>Query embedded → compare to indexed doc embeddings → return top-k similar chunks. No keyword matching.</div>
    </div>
    <div class="tip"><span class="icon">💡</span>Java Parallel: A vector store is like a HashMap&lt;Float[], Document&gt; but with approximate nearest-neighbor search instead of exact key lookup.</div>
  </div>
</div>

<!-- ─── PART B: AGENTIC ARCHITECTURES (Weeks 7–12) ─── -->
<h3 class="section">🤖 PART B: Agentic Architectures & Frameworks (Weeks 7–12)</h3>

<div class="week">
  <div class="week-header w7"><span class="week-num">Week 7</span> Agentic Tools in Python (LangChain Intro)</div>
  <div class="week-body">
    <div class="summary">🔵 <strong>Core Idea:</strong> LangChain provides a 5-layer architecture (Models → Prompts → Chains → Memory → Agents) that transforms standalone LLM calls into composable, stateful, tool-using pipelines. LCEL uses the pipe operator <code>|</code> for functional chain composition.</div>
    <div class="concepts">
      <div class="concept c-blue"><strong>🔗 LangChain LCEL</strong><code>chain = prompt | llm | parser</code>. Pipe operator composes Runnables. Supports async, streaming, batching natively.</div>
      <div class="concept c-green"><strong>🛠️ Tool Calling</strong><code>@tool</code> decorator wraps Python functions. Agent decides WHEN to call which tool based on reasoning.</div>
      <div class="concept c-orange"><strong>💬 Prompt Templates</strong><code>ChatPromptTemplate.from_messages([...])</code>. Dynamic placeholders injected at runtime from session state.</div>
      <div class="concept c-red"><strong>📤 Output Parsers</strong><code>StrOutputParser</code>, <code>PydanticOutputParser</code>. Converts raw LLM text → typed Python objects.</div>
    </div>
    <div class="tip"><span class="icon">⚠️</span>Critical: Use <code>ainvoke()</code> not <code>invoke()</code> in async agents. Synchronous invoke() blocks the event loop under concurrent load.</div>
  </div>
</div>

<div class="week">
  <div class="week-header w8"><span class="week-num">Week 8</span> Introduction to Agentic AI</div>
  <div class="week-body">
    <div class="summary">🟠 <strong>Core Idea:</strong> An agent = LLM + Tools + Memory + Goal. The agent continuously loops through Perception → Planning → Action → Observation until the objective is achieved or a stopping condition is met.</div>
    <div class="concepts">
      <div class="concept c-orange"><strong>🎯 Agent Definition</strong>Autonomous system that perceives environment, reasons, acts, and observes consequences. Not a one-shot call.</div>
      <div class="concept c-blue"><strong>🔄 Agent Lifecycle</strong>Goal → Plan → Tool Selection → Tool Execution → Observe Result → Re-plan → Repeat until done.</div>
      <div class="concept c-green"><strong>📊 4 Autonomy Levels</strong>L1: Simple reflex. L2: Model-based. L3: Goal-based. L4: Utility-based (optimal decision-maker).</div>
      <div class="concept c-red"><strong>🔧 Single vs Multi-Agent</strong>Single: one reasoning loop. Multi: specialized agents collaborate. Multi = higher capability, higher complexity.</div>
    </div>
    <div class="tip"><span class="icon">💡</span>Java Parallel: An agent is like a Spring Batch Job with dynamic step selection—each step (tool) is chosen at runtime by the LLM "processor" based on observed output.</div>
  </div>
</div>

<div class="week">
  <div class="week-header w9"><span class="week-num">Week 9</span> Programming Frameworks for Agentic Systems</div>
  <div class="week-body">
    <div class="summary">🟢 <strong>Core Idea:</strong> Six major frameworks exist for building agentic systems. LangChain dominates tool orchestration; CrewAI excels at role-based multi-agent teams; AutoGen shines for conversational code-generation workflows.</div>
    <div class="concepts">
      <div class="concept c-green"><strong>🔗 LangChain</strong>Universal orchestration. Largest ecosystem. Best for RAG + tool chains + memory management.</div>
      <div class="concept c-blue"><strong>⚓ CrewAI</strong>Role-based multi-agent. Agent → Task → Crew triad. Sequential or hierarchical process modes.</div>
      <div class="concept c-orange"><strong>🤝 AutoGen</strong>Microsoft. ConversableAgent + GroupChat. Excels at LLM-driven code writing and self-debugging loops.</div>
      <div class="concept c-purple"><strong>🔍 Haystack</strong>Specialized for NLP pipelines and document processing. Strong retrieval components.</div>
      <div class="concept c-red"><strong>🧠 DSPy</strong>Programmatic prompt optimization. Compiles prompts like code, uses training data to auto-optimize instructions.</div>
      <div class="concept c-pink"><strong>🏢 Semantic Kernel</strong>Microsoft enterprise SDK. Strong C# / Java / Python support. Azure-native integration.</div>
    </div>
    <div class="tip"><span class="icon">⚠️</span>Framework vs SDK: Frameworks give opinionated structure (CrewAI, AutoGen). SDKs give raw building blocks (LangChain Core). Choose based on workflow predictability needs.</div>
  </div>
</div>

<div class="week">
  <div class="week-header w10"><span class="week-num">Week 10</span> Agent Architectures & Collaboration</div>
  <div class="week-body">
    <div class="summary">🟣 <strong>Core Idea:</strong> Agent architectures range from reactive (stimulus-response) to deliberative (plan then act) to BDI (Belief-Desire-Intention). Multi-agent collaboration patterns—cooperative, competitive, and coordinated—solve complex tasks no single agent can handle.</div>
    <div class="concepts">
      <div class="concept c-purple"><strong>⚡ Reactive Architecture</strong>Direct stimulus → action. No internal model. Fast, fault-tolerant. Used for high-frequency trading alerts.</div>
      <div class="concept c-blue"><strong>🗺️ Deliberative Architecture</strong>Build internal world model → plan → execute. ReAct agents are deliberative (Think → Act → Observe).</div>
      <div class="concept c-green"><strong>🧠 BDI Architecture</strong>Beliefs (world state) + Desires (goals) + Intentions (committed plans). Most sophisticated agent model.</div>
      <div class="concept c-orange"><strong>🤝 Cooperative Agents</strong>Shared goal, complementary roles. Crew members work together. Sum > parts.</div>
      <div class="concept c-red"><strong>🏆 Competitive Agents</strong>Adversarial debate agents: one proposes, one critiques. Improves output quality through disagreement.</div>
      <div class="concept c-pink"><strong>🎯 Coordinated Agents</strong>Orchestrator assigns tasks to specialists. Hierarchical process in CrewAI uses a manager LLM as coordinator.</div>
    </div>
    <div class="tip"><span class="icon">🔴</span>Critical Anti-Pattern: NEVER set <code>allow_delegation=True</code> on peer agents in a sequential crew. Creates circular delegation deadlocks consuming 1M+ tokens in minutes.</div>
  </div>
</div>

<div class="week">
  <div class="week-header w11"><span class="week-num">Week 11</span> Decision Making & Planning in Agents</div>
  <div class="week-body">
    <div class="summary">💡 <strong>Core Idea:</strong> The ReAct (Reason + Act) framework structures agent decision-making as interleaved Thought → Action → Observation loops, enabling transparent multi-step reasoning. Hierarchical task networks decompose complex goals into executable sub-tasks.</div>
    <div class="concepts">
      <div class="concept c-red"><strong>⚡ ReAct Pattern</strong>Thought: "I need today's rate." → Act: <code>get_rate(currency="USD")</code> → Observe: "1 USD = 84.2 INR" → Thought: "Now compute..."</div>
      <div class="concept c-blue"><strong>🌲 Hierarchical Planning</strong>Goal → Sub-goals → Tasks → Actions. DAG structure. Each node is deterministically executed.</div>
      <div class="concept c-green"><strong>🎮 Reactive Planning</strong>No pre-planned path. React to real-time observations. Good for dynamic environments.</div>
      <div class="concept c-orange"><strong>🔄 Reinforcement Loop</strong>Agent acts → environment gives reward → agent updates policy. Used for self-improving adaptive agents.</div>
    </div>
    <div class="tip"><span class="icon">💡</span>ReAct is the dominant production pattern. It provides explainable reasoning traces that can be logged for debugging, compliance auditing, and trust.</div>
  </div>
</div>

<div class="week">
  <div class="week-header w12"><span class="week-num">Week 12</span> Memory & Knowledge Retrieval in Agents + MCP</div>
  <div class="week-body">
    <div class="summary">🔵 <strong>Core Idea:</strong> Agents have two memory tiers: Short-Term Memory (the context window, ephemeral) and Long-Term Memory (vector stores + databases, persistent). MCP (Model Context Protocol) by Anthropic provides a universal JSON-RPC 2.0 interface for agents to securely discover and invoke external tools.</div>
    <div class="concepts">
      <div class="concept c-blue"><strong>🧠 Short-Term Memory (STM)</strong>The active context window. <code>ConversationBufferWindowMemory(k=5)</code> keeps last k turns verbatim. Fast, expensive.</div>
      <div class="concept c-green"><strong>🗄️ Long-Term Memory (LTM)</strong>FAISS / Chroma vector store + SQL database. Persists across sessions. Retrieved via semantic similarity search.</div>
      <div class="concept c-orange"><strong>📡 Model Context Protocol (MCP)</strong>Anthropic Nov 2024. JSON-RPC 2.0 over stdio or HTTP-SSE. Universal tool gateway. Like JDBC for AI tools.</div>
      <div class="concept c-purple"><strong>🔌 A2A Communication</strong>Agent-to-Agent protocol. Structured message passing. Enables typed cross-agent tool invocations.</div>
      <div class="concept c-red"><strong>💾 Memory Strategy</strong>SummaryBuffer: recent turns verbatim + old turns summarized. Best balance for long conversations.</div>
      <div class="concept c-pink"><strong>📚 Knowledge Graphs</strong>Entity → Relationship → Entity triples. Enables multi-hop relational reasoning beyond dense vector similarity.</div>
    </div>
    <div class="tip"><span class="icon">⚠️</span>MCP Gotcha: Tool schemas must use Pydantic v2 with strict type coercion. An agent passing string "36" where int 36 is expected causes silent SQL type errors downstream.</div>
  </div>
</div>

<!-- ─── PART C: ADVANCED COGNITION (Weeks 13–16) ─── -->
<h3 class="section">🧪 PART C: Cognitive Engineering, RAG & Deployment (Weeks 13–16)</h3>

<div class="week">
  <div class="week-header w13"><span class="week-num">Week 13</span> Prompt Engineering & Adaptive Instructions</div>
  <div class="week-body">
    <div class="summary">🟡 <strong>Core Idea:</strong> Prompts are the primary "code" for programming LLM behaviour. Well-structured prompts with system role, few-shot examples, and output format constraints dramatically improve reliability and enable dynamic adaptation at inference time.</div>
    <div class="concepts">
      <div class="concept c-orange"><strong>🎯 Zero-Shot Prompting</strong>Direct instruction with no examples. Works for simple tasks. Fails for complex multi-step reasoning.</div>
      <div class="concept c-blue"><strong>📝 Few-Shot Prompting</strong>3–5 input→output examples in the prompt. Dramatically improves structured output adherence.</div>
      <div class="concept c-green"><strong>🔗 Chain-of-Thought (CoT)</strong>"Think step by step." Forces intermediate reasoning. Reduces arithmetic and logic errors by 40–60%.</div>
      <div class="concept c-red"><strong>🔧 Dynamic Prompts</strong>Runtime template injection. Agent's learned user preferences injected as bullet constraints into system prompt.</div>
      <div class="concept c-purple"><strong>🧩 Modular Prompts</strong>Base system prompt + role-specific module + task-specific module + output format module. Composable.</div>
    </div>
    <div class="tip"><span class="icon">💡</span>Java Parallel: Dynamic prompts = Spring Boot <code>@Value</code> injection at runtime. The system prompt is the application.properties of an agent.</div>
  </div>
</div>

<div class="week">
  <div class="week-header w14"><span class="week-num">Week 14</span> Learning & Adaptation in Agents</div>
  <div class="week-body">
    <div class="summary">🟢 <strong>Core Idea:</strong> Agents can adapt through in-context learning (no weight changes) or fine-tuning (weight updates). RLHF (Reinforcement Learning from Human Feedback) transforms human preference ratings into reward signals that steer model outputs towards desired behaviors.</div>
    <div class="concepts">
      <div class="concept c-green"><strong>🔄 Hardcoded vs Adaptive</strong>Hardcoded: fixed rules (fast, predictable). Adaptive: learns from feedback (slower, more powerful).</div>
      <div class="concept c-blue"><strong>🎯 RLHF Pipeline</strong>Collect human preference data → Train Reward Model → Fine-tune LLM with PPO to maximize reward score.</div>
      <div class="concept c-orange"><strong>🎲 Exploration vs Exploitation</strong>ε-greedy: explore random actions with prob ε, exploit best known with (1-ε). Prevents getting stuck in local optima.</div>
      <div class="concept c-red"><strong>📊 Model-Free vs Model-Based RL</strong>Model-free: learns directly from experience (Q-learning). Model-based: builds environment model first. Agents need both.</div>
      <div class="concept c-purple"><strong>🧠 Adaptive Feedback Engine</strong>Store user corrections → persist as preference rules → inject into system prompt as runtime constraints.</div>
    </div>
    <div class="tip"><span class="icon">💡</span>Production Pattern: Store up to 7 active user preference rules (LRU eviction). Inject into every system prompt. Agent "learns" without any weight updates or fine-tuning cost.</div>
  </div>
</div>

<div class="week">
  <div class="week-header w15"><span class="week-num">Week 15</span> Retrieval-Augmented Generation (RAG)</div>
  <div class="week-body">
    <div class="summary">🔵 <strong>Core Idea:</strong> RAG = LLM + Search. Instead of relying on parametric (baked-in) knowledge, RAG retrieves fresh, grounded context from an external knowledge base at inference time. This eliminates hallucinations on domain-specific topics without fine-tuning.</div>
    <div class="concepts">
      <div class="concept c-blue"><strong>📄 Document Ingestion</strong>Load docs → Split chunks (800 chars, 150 overlap) → Embed chunks → Index in FAISS → Save to disk.</div>
      <div class="concept c-green"><strong>🔍 Retrieval Pipeline</strong>User query → Embed query → kNN search (k=4, cosine distance) → Return top chunks as context.</div>
      <div class="concept c-orange"><strong>🤖 Grounded Generation</strong>System prompt: "Answer ONLY using provided context. If not in context, say 'I don't know.'" Prevents hallucination.</div>
      <div class="concept c-red"><strong>💬 Conversational RAG</strong><code>ConversationalRetrievalChain</code>: condenses follow-up questions into standalone queries before retrieval.</div>
      <div class="concept c-purple"><strong>📊 RAG Triad Evaluation</strong>Faithfulness (grounded?) + Answer Relevance (addresses question?) + Context Recall (right docs retrieved?) = RAG quality score.</div>
      <div class="concept c-pink"><strong>⚡ Hybrid Retrieval</strong>Dense (semantic) + Sparse (BM25 keyword) combined. Handles both semantic similarity AND exact keyword matching.</div>
    </div>
    <div class="tip"><span class="icon">🔴</span>Anti-Hallucination Rule: Always include <code>source_documents</code> in agent responses. Force citation of retrieved chunk names. Users can verify grounding independently.</div>
  </div>
</div>

<div class="week">
  <div class="week-header w16"><span class="week-num">Week 16</span> Deploying & Monitoring Agentic Systems</div>
  <div class="week-body">
    <div class="summary">💗 <strong>Core Idea:</strong> Production deployment requires a lifecycle: Build → Containerize → Deploy → Monitor → Improve. FastAPI wraps agents as REST microservices; LangSmith provides distributed tracing; Kubernetes enables horizontal scaling under load.</div>
    <div class="concepts">
      <div class="concept c-pink"><strong>🚀 FastAPI Deployment</strong><code>@app.post("/agent")</code>. Async endpoints. OpenAPI docs auto-generated. JWT middleware for auth.</div>
      <div class="concept c-blue"><strong>🐳 Containerization</strong>Dockerfile → Docker image → Kubernetes pod. Resource limits prevent agent runaway (CPU/Memory caps).</div>
      <div class="concept c-green"><strong>📈 LangSmith Tracing</strong>End-to-end trace: input → each LLM call → tool execution → output. Token count + latency + cost per step.</div>
      <div class="concept c-orange"><strong>☁️ Cloud Platforms</strong>AWS Bedrock (managed LLMs), AWS SageMaker (fine-tuning), HuggingFace Spaces (cheap demos).</div>
      <div class="concept c-red"><strong>🔄 Rolling Deployment</strong>Blue-Green: run v1 and v2 simultaneously, switch traffic. Prevents downtime during agent version upgrades.</div>
    </div>
    <div class="tip"><span class="icon">💡</span>Monitoring Checklist: Track latency (p50/p95/p99), token usage per session, tool error rates, and guardrail trigger frequency. Alert on anomalous token spikes immediately.</div>
  </div>
</div>

<!-- ─── PART D: EVALUATION & GOVERNANCE (Weeks 17–21) ─── -->
<h3 class="section">⚖️ PART D: Evaluation, Ethics & Capstone (Weeks 17–21)</h3>

<div class="week">
  <div class="week-header w17"><span class="week-num">Week 17</span> Agent Evaluation & Debugging</div>
  <div class="week-body">
    <div class="summary">🟣 <strong>Core Idea:</strong> Agents are non-deterministic systems. Evaluation requires multi-dimensional metrics covering task success, output quality, retrieval accuracy, and operational efficiency. LLM-as-Judge uses a second LLM to automatically score outputs against a rubric.</div>
    <div class="concepts">
      <div class="concept c-purple"><strong>📊 Evaluation Dimensions</strong>Task Success Rate · Response Coherence · Answer Correctness · Context Coverage · Latency · Cost per Query.</div>
      <div class="concept c-blue"><strong>🤖 LLM-as-Judge</strong>Use GPT-4 to score agent outputs on faithfulness, relevance, and helpfulness. Scales evaluation without human annotators.</div>
      <div class="concept c-orange"><strong>🔍 RAG Debugging</strong>"RAG Dilemma": retrieved chunks exist but agent ignores them. Fix: reranking + strict prompt grounding constraints.</div>
      <div class="concept c-green"><strong>🛠️ LangSmith Debugging</strong>Full trace replay. Identify which tool call failed, which LLM step hallucinated, and at what token count.</div>
      <div class="concept c-red"><strong>📉 Regression Testing</strong>Maintain golden test set of 50+ query→expected_answer pairs. Run after every agent update. Catch regressions before prod.</div>
    </div>
    <div class="tip"><span class="icon">💡</span>Golden Rule of Agent Evaluation: "If you can't measure it, you can't improve it." Define RAG Triad scores before deploying any RAG agent to production.</div>
  </div>
</div>

<div class="week">
  <div class="week-header w18"><span class="week-num">Week 18</span> Ethics, Safety & Governance in Agentic AI</div>
  <div class="week-body">
    <div class="summary">🔴 <strong>Core Idea:</strong> Production agents carry legal and ethical obligations. Responsible AI requires Fairness, Accountability, Transparency, and Safety (FACTS) guardrails built into the architecture—not bolted on as afterthoughts. Context drift and prompt injection are the two primary attack vectors.</div>
    <div class="concepts">
      <div class="concept c-red"><strong>🛡️ Safety Guardrails</strong>Pre-execution lexical firewall: block prohibited keywords BEFORE LLM call. Zero token cost. 100% deterministic.</div>
      <div class="concept c-orange"><strong>💉 Prompt Injection Defense</strong>Adversarial: "Ignore previous instructions." Defense: pre-inference sanitizer + immutable system prompt prefix.</div>
      <div class="concept c-blue"><strong>⚖️ Fairness</strong>Audit model outputs across demographic groups. Use diverse evaluation datasets. Monitor for disparate impact.</div>
      <div class="concept c-green"><strong>🔍 Transparency</strong>Log all agent decisions with full reasoning trace. Users must be able to appeal and understand agent decisions.</div>
      <div class="concept c-purple"><strong>🔒 PII Governance</strong>Pre-log regex scrubbing: credit cards, Aadhaar, PAN, emails. Never write raw PII to any log sink.</div>
      <div class="concept c-pink"><strong>🌊 Context Drift</strong>Agent gradually loses original objective over long multi-step tasks. Fix: periodic objective re-injection and step counters.</div>
    </div>
    <div class="tip"><span class="icon">🔴</span>Regulatory: PCI-DSS Level 1 = no raw card numbers in logs. GDPR Art.33 = report breach within 72h. RBI IT Guidelines = immutable audit trail for all financial agent decisions.</div>
  </div>
</div>

<div class="week">
  <div class="week-header w19"><span class="week-num">Week 19</span> Real-World Applications & Case Studies</div>
  <div class="week-body">
    <div class="summary">🔵 <strong>Core Idea:</strong> Agentic AI is deployed across all industries. Real-world agents combine RAG, tool use, memory, and safety guardrails into domain-specific pipelines. Each industry has unique safety requirements and data constraints that shape agent architecture decisions.</div>
    <div class="concepts">
      <div class="concept c-blue"><strong>🏦 Finance Agents</strong>Portfolio analysis, fraud detection, loan underwriting. Must refuse unauthorized transactions. Human escalation mandatory.</div>
      <div class="concept c-green"><strong>🏥 Healthcare Triage Agents</strong>Symptom assessment → risk classification → triage priority. HIPAA compliance. No diagnosis—only information.</div>
      <div class="concept c-orange"><strong>🏭 Manufacturing IoT Agents</strong>Sensor anomaly detection → maintenance alert → work order creation. Integrate with SCADA systems via MCP.</div>
      <div class="concept c-red"><strong>🛒 E-Commerce Agents</strong>Product discovery, return processing, inventory queries. Policy RAG chatbot is the most common deployment pattern.</div>
      <div class="concept c-purple"><strong>📚 Education Agents</strong>Adaptive tutoring, personalized quiz generation, learning path optimization. Socratic dialogue pattern.</div>
    </div>
    <div class="tip"><span class="icon">💡</span>Cross-Industry Insight: All production agents share the same 4-layer architecture: Safety Guardrail → Cognitive Routing → Deterministic Tools → PII Telemetry. Domain specifics live in the tool layer.</div>
  </div>
</div>

<div class="week">
  <div class="week-header w20"><span class="week-num">Week 20</span> Low-Code / No-Code Tools: LangFlow & Flowise</div>
  <div class="week-body">
    <div class="summary">🟢 <strong>Core Idea:</strong> Visual pipeline builders democratize agent construction. LangFlow provides a drag-and-drop interface equivalent to writing LangChain Python code but without programming. These tools accelerate prototyping but have limited flexibility for production-grade safety and error handling.</div>
    <div class="concepts">
      <div class="concept c-green"><strong>🎨 LangFlow</strong>Drag-and-drop RAG builder. Each visual node = LangChain component. Export as JSON or deploy directly as API.</div>
      <div class="concept c-blue"><strong>🌊 Flowise (Legacy)</strong>Node.js visual builder. Note: Flowise has reached end-of-life (Aug 2026). Use LangFlow for new builds.</div>
      <div class="concept c-orange"><strong>📊 Visual vs Code</strong>Visual: fast prototyping, great demos, limited production safety. Code: full control, unit-testable, CI/CD compatible.</div>
      <div class="concept c-purple"><strong>🔌 LangFlow Components</strong>Document Loader → Text Splitter → Embedding Model → Vector Store → Retriever → LLM → Response Output.</div>
    </div>
    <div class="tip"><span class="icon">⚠️</span>LangFlow Usage: Install via <code>pip install langflow</code> then <code>langflow run</code> → open http://127.0.0.1:7860. Import JSON flows for version-controlled agent templates.</div>
  </div>
</div>

<div class="week">
  <div class="week-header w21"><span class="week-num">Week 21</span> Capstone: Design, Build & Evaluate an AI Agent</div>
  <div class="week-body">
    <div class="summary">🟣 <strong>Core Idea:</strong> The capstone requires end-to-end AI engineering: choose an industry scenario, design a safety-first architecture, implement with a recognized framework (LangChain/CrewAI/AutoGen), build evaluation criteria, test failure modes, and justify architectural decisions with evidence.</div>
    <div class="concepts">
      <div class="concept c-purple"><strong>🏗️ Architecture Requirements</strong>Must demonstrate: multi-step reasoning, tool use, memory management, safety guardrails, and grounded generation.</div>
      <div class="concept c-blue"><strong>📋 Evaluation Criteria</strong>Success Rate · Safety Compliance · Latency SLA · RAG Triad Score · Token Budget Adherence · Human Escalation Rate.</div>
      <div class="concept c-orange"><strong>🎯 Track A: Framework-Based</strong>LangFlow (recommended), Make.com, Relevance AI, LangChain, CrewAI. Full visual or code implementation.</div>
      <div class="concept c-green"><strong>🔧 Track B: Framework-Free</strong>Justify custom architecture. Must prove equivalent capabilities through test logs and architecture documentation.</div>
      <div class="concept c-red"><strong>⚠️ Failure Mode Documentation</strong>Must document: what failures were anticipated, how they were prevented, and what escalation paths exist for edge cases.</div>
      <div class="concept c-pink"><strong>📊 Submission Artifacts</strong>Architecture diagram + Code + Conversation logs + Evaluation scorecard + Video demo + Reflection document.</div>
    </div>
    <div class="tip"><span class="icon">💡</span>Capstone Pro-Tip: The strongest submissions demonstrate a REAL failure mode (e.g., circular delegation, hallucinated math), show how it was detected and fixed, and prove the fix works through test logs.</div>
  </div>
</div>

<!-- MASTER CHEAT SHEET -->
<h3 class="section">📋 MASTER CHEAT SHEET — Production Agent Blueprint</h3>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px;">
  <div style="background:#0f172a;color:#f8fafc;border-radius:10px;padding:18px;font-family:'Fira Code',monospace;font-size:.82rem;line-height:1.6;border:1.5px solid #334155;">
<span style="color:#64748b;"># PRODUCTION SAFE AGENT PIPELINE</span>
<span style="color:#f43f5e;">class</span> <span style="color:#38bdf8;">AgentOrchestrator</span>:
  <span style="color:#a78bfa;">async def</span> run(self, query, budget):
    <span style="color:#64748b;"># 1. Safety firewall FIRST</span>
    if self.guardrail.check(query):
      return SafetyBlock

    <span style="color:#64748b;"># 2. Budget tripwire</span>
    await budget.consume(300)

    <span style="color:#64748b;"># 3. Async tool (non-blocking)</span>
    result = await asyncio.to_thread(
      DeterministicTool.calculate, input)

    <span style="color:#64748b;"># 4. Grounded LLM response</span>
    response = await llm.ainvoke(msgs)

    <span style="color:#64748b;"># 5. PII scrub before logging</span>
    return sanitize_pii(response)
  </div>
  <div style="padding:0 8px;">
    <div style="background:#fef2f2;border:1.5px solid #ef4444;border-radius:8px;padding:12px 14px;margin-bottom:10px;">
      <strong style="color:#dc2626;font-family:'Kalam',cursive;font-size:1rem;">🔴 NEVER DO These</strong>
      <div style="font-size:.88rem;margin-top:6px;line-height:1.7;">
        ❌ Synchronous I/O in async agent<br>
        ❌ allow_delegation=True on peer agents<br>
        ❌ No token budget cap on sessions<br>
        ❌ LLM doing math calculations<br>
        ❌ Raw PII written to any log
      </div>
    </div>
    <div style="background:#f0fdf4;border:1.5px solid #10b981;border-radius:8px;padding:12px 14px;">
      <strong style="color:#065f46;font-family:'Kalam',cursive;font-size:1rem;">🟢 ALWAYS DO These</strong>
      <div style="font-size:.88rem;margin-top:6px;line-height:1.7;">
        ✅ temperature=0.1 for tool nodes<br>
        ✅ Pydantic v2 on all tool inputs<br>
        ✅ asyncio.to_thread for sync calls<br>
        ✅ Circuit breaker on LLM calls<br>
        ✅ RAG Triad scoring before prod
      </div>
    </div>
  </div>
</div>

<!-- Quick Reference Table -->
<table style="font-size:.88rem;margin-bottom:8px;">
  <tr style="background:#1e293b;color:#f8fafc;">
    <th>Framework</th><th>Best For</th><th>Key Class</th><th>Watch Out For</th>
  </tr>
  <tr><td><strong>LangChain LCEL</strong></td><td>RAG pipelines, tool chains</td><td>RunnableSequence</td><td>Fallback swallowing errors</td></tr>
  <tr><td><strong>CrewAI</strong></td><td>Role-based multi-agent teams</td><td>Agent/Task/Crew</td><td>Circular delegation deadlocks</td></tr>
  <tr><td><strong>AutoGen</strong></td><td>Code generation debates</td><td>ConversableAgent</td><td>Missing max_consecutive_auto_reply</td></tr>
  <tr><td><strong>MCP</strong></td><td>Universal tool gateway</td><td>JSON-RPC 2.0 server</td><td>Missing Pydantic schema validation</td></tr>
  <tr><td><strong>FAISS</strong></td><td>Fast vector similarity search</td><td>FAISS.from_documents</td><td>Stale index when docs update</td></tr>
  <tr><td><strong>LangSmith</strong></td><td>Tracing & evaluation</td><td>traceable decorator</td><td>Can expose sensitive prompts in logs</td></tr>
</table>

<footer>
  <strong>IIT Madras Pravartak — Professional Certificate Programme in Agentic AI & Applications</strong><br>
  21-Week Master Notebook · Python · LangChain · CrewAI · AutoGen · RAG · MCP · Production Deployment<br>
  <span style="font-size:.8rem;color:#94a3b8;">Generated: Beautiful Handwritten Notebook Edition · For Enterprise Java Developers Transitioning to Agentic AI</span>
</footer>

</div>
</body>
</html>
"""

# Write HTML
HTML_OUT.write_text(HTML, encoding="utf-8")
print(f"HTML generated: {HTML_OUT} ({len(HTML):,} bytes)")

# Compile to PDF via Edge headless
print("Compiling PDF via Edge headless...")
result = subprocess.run(
    [EDGE, "--headless", "--disable-gpu",
     f"--print-to-pdf={str(PDF_OUT)}",
     f"file:///{str(HTML_OUT).replace(os.sep, '/')}"],
    capture_output=True, text=True
)
if PDF_OUT.exists():
    print(f"SUCCESS: {PDF_OUT} ({PDF_OUT.stat().st_size:,} bytes)")
else:
    print(f"PDF failed: {result.stderr}")
