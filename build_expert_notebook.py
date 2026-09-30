"""
IITM Agentic AI — Expert-Level Practical Notebook
Goal: Interview-ready · Project-executable · Team-leadable · Architect-thinking
"""
import os, sys, subprocess
from pathlib import Path

WORKSPACE = Path(r"C:\Users\Maharshi\Documents\IITM_Agentic")
HTML_OUT = WORKSPACE / "IITM_Expert_Practical_Notebook.html"
PDF_OUT  = WORKSPACE / "IITM_Expert_Practical_Notebook.pdf"
EDGE     = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>IITM Agentic AI — Expert Practical Notebook</title>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Kalam:wght@400;700&family=Fira+Code:wght@400;600&family=Patrick+Hand&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{background:#f0ebe0;font-family:'Patrick Hand','Caveat',cursive;font-size:15.5px;line-height:1.65;color:#1e293b;padding:20px;}
.notebook{max-width:1120px;margin:0 auto;background:#fffef9;
  background-image:linear-gradient(90deg,rgba(220,38,38,.18) 0 2px,transparent 2px),linear-gradient(#dde4ef 1px,transparent 1px);
  background-size:68px 100%,100% 34px;background-position:60px 0,0 12px;
  border-radius:14px;box-shadow:0 8px 40px rgba(0,0,0,.18),4px 0 0 #f59e0b inset;
  padding:50px 55px 60px 90px;position:relative;}
.notebook::before{content:'';position:absolute;top:50px;left:26px;bottom:50px;width:14px;
  background:radial-gradient(circle,#bbb 5px,transparent 6px);background-size:14px 110px;}
.cover{text-align:center;padding:40px 20px 50px;border-bottom:3px double #f59e0b;margin-bottom:40px;}
.cover-badge{display:inline-block;padding:5px 18px;border-radius:20px;font-size:.85rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;background:#1e40af;color:#fff;margin-bottom:15px;}
.cover h1{font-family:'Kalam',cursive;font-size:2.8rem;color:#0f172a;text-shadow:2px 2px 0 #fde68a;margin:10px 0;}
.cover h2{font-size:1.4rem;color:#475569;font-weight:400;margin:8px 0;}
.cover p{font-size:.95rem;color:#64748b;margin-top:10px;}
.meta-chips{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin-top:16px;}
.chip{padding:4px 12px;border-radius:999px;font-size:.78rem;font-weight:700;border:1.5px solid;}
.chip-blue{background:#eff6ff;color:#1d4ed8;border-color:#3b82f6;}
.chip-green{background:#f0fdf4;color:#065f46;border-color:#10b981;}
.chip-orange{background:#fff7ed;color:#c2410c;border-color:#f97316;}
.chip-purple{background:#faf5ff;color:#6b21a8;border-color:#a855f7;}
.chip-red{background:#fef2f2;color:#991b1b;border-color:#ef4444;}
/* Week Card */
.week{margin:28px 0;border-radius:12px;overflow:hidden;box-shadow:0 4px 16px rgba(0,0,0,.07);border:1.5px solid #e2e8f0;}
.week-header{padding:13px 20px;display:flex;align-items:center;gap:14px;font-family:'Kalam',cursive;font-size:1.25rem;font-weight:700;color:#fff;}
.week-num{background:rgba(255,255,255,.25);border-radius:8px;padding:3px 10px;font-size:1rem;white-space:nowrap;}
.week-body{background:#fff;padding:16px 22px;}
/* Color headers */
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
/* Content blocks */
.summary{background:#f8fafc;border-left:5px solid #f59e0b;border-radius:0 8px 8px 0;padding:9px 15px;margin-bottom:12px;font-size:.97rem;}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-bottom:10px;}
.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:9px;margin-bottom:10px;}
.concept{padding:9px 13px;border-radius:8px;font-size:.88rem;border:1px solid #e2e8f0;}
.c-red{background:#fef2f2;border-left:4px solid #ef4444;}
.c-blue{background:#eff6ff;border-left:4px solid #3b82f6;}
.c-green{background:#f0fdf4;border-left:4px solid #10b981;}
.c-orange{background:#fff7ed;border-left:4px solid #f97316;}
.c-purple{background:#faf5ff;border-left:4px solid #a855f7;}
.c-pink{background:#fdf2f8;border-left:4px solid #ec4899;}
.c-teal{background:#f0fdfa;border-left:4px solid #0d9488;}
.c-yellow{background:#fefce8;border-left:4px solid #ca8a04;}
.concept strong{display:block;font-family:'Kalam',cursive;font-size:.97rem;color:#0f172a;margin-bottom:3px;}
/* Special sections */
.practical{background:#0f172a;border-radius:10px;padding:14px 18px;margin:10px 0;color:#f8fafc;font-size:.85rem;}
.practical .ptitle{font-family:'Kalam',cursive;font-size:1.05rem;color:#38bdf8;margin-bottom:8px;display:flex;align-items:center;gap:6px;}
.practical pre{font-family:'Fira Code',monospace;font-size:.8rem;line-height:1.5;white-space:pre-wrap;word-break:break-all;}
.kw{color:#f43f5e;} .fn{color:#38bdf8;} .st{color:#a3e635;} .cm{color:#64748b;} .kl{color:#fb923c;} .nm{color:#e879f9;}
.interview{background:linear-gradient(135deg,#fffbeb,#fef3c7);border:1.5px solid #fbbf24;border-radius:10px;padding:12px 16px;margin:10px 0;}
.interview .ititle{font-family:'Kalam',cursive;font-size:1rem;color:#92400e;margin-bottom:7px;}
.interview .qa{margin-bottom:7px;font-size:.88rem;}
.interview .q{color:#1e40af;font-weight:700;margin-bottom:2px;}
.interview .a{color:#1e293b;padding-left:12px;border-left:2px solid #fbbf24;}
.architect{background:linear-gradient(135deg,#f0fdf4,#dcfce7);border:1.5px solid #16a34a;border-radius:10px;padding:12px 16px;margin:10px 0;}
.architect .atitle{font-family:'Kalam',cursive;font-size:1rem;color:#065f46;margin-bottom:7px;}
.architect ul{padding-left:16px;font-size:.88rem;line-height:1.7;}
.tip{display:flex;gap:8px;align-items:flex-start;padding:8px 12px;border-radius:6px;background:#fffbeb;border:1px dashed #fbbf24;font-size:.85rem;margin-top:8px;}
.tip .icon{font-size:1.1rem;flex-shrink:0;}
code{font-family:'Fira Code',monospace;font-size:.82em;background:#1e293b;color:#38bdf8;padding:2px 5px;border-radius:4px;}
h3.section{font-family:'Kalam',cursive;font-size:1.5rem;color:#0f172a;border-bottom:2px solid #fde68a;padding-bottom:5px;margin:36px 0 18px;display:flex;align-items:center;gap:10px;}
.cheatsheet{background:#0f172a;border-radius:12px;padding:20px;color:#f8fafc;margin-top:12px;}
.cheatsheet h4{font-family:'Kalam',cursive;color:#38bdf8;font-size:1.1rem;margin-bottom:10px;}
table{width:100%;border-collapse:collapse;margin:12px 0;background:#fff;border-radius:8px;overflow:hidden;font-size:.85rem;}
th,td{padding:9px 14px;border:1px solid #e2e8f0;text-align:left;}
th{background:#f1f5f9;color:#0f172a;font-weight:700;}
tr:nth-child(even){background:#f8fafc;}
footer{text-align:center;margin-top:40px;padding:18px;border-top:2px dashed #cbd5e1;color:#64748b;font-size:.87rem;}
@media print{body{background:#fff;padding:0;}.notebook{box-shadow:none;background-image:none;padding:15px 20px 20px 35px;}.notebook::before{display:none;}.week{break-inside:avoid;page-break-inside:avoid;}h3.section{page-break-before:auto;}}
</style>
</head>
<body>
<div class="notebook">

<div class="cover">
  <div class="cover-badge">🏛️ IIT Madras Pravartak — Professional Certificate</div>
  <h1>Agentic AI & Applications</h1>
  <h2>Expert-Level Practical Notebook — Interview · Projects · Architecture · Leadership</h2>
  <p>Read once. Clear any interview. Execute any project. Lead any AI team.</p>
  <div class="meta-chips">
    <span class="chip chip-blue">🧠 Thinking Like an AI Architect</span>
    <span class="chip chip-green">🛠️ Build Any Real Project</span>
    <span class="chip chip-orange">🎯 Crack Any Interview</span>
    <span class="chip chip-purple">👑 Lead Engineering Teams</span>
    <span class="chip chip-red">⚠️ Avoid Production Disasters</span>
  </div>
</div>

<h3 class="section">🎨 PART A: Foundations — Python, AI & LLMs (Weeks 1–6)</h3>

<!-- WEEK 1 -->
<div class="week">
<div class="week-header w1"><span class="week-num">Week 1</span> Getting Started: Python & ChatGPT</div>
<div class="week-body">
<div class="summary">🔴 ChatGPT is NOT magic — it is a token prediction engine using self-attention over a context window. Temperature controls randomness. Python is your control plane for every AI system.</div>
<div class="grid2">
  <div class="concept c-red"><strong>🐍 Python as AI Control Plane</strong>Every LLM call, embedding, vector search, and agent loop is Python code. Master it like Java — it IS the backend.</div>
  <div class="concept c-blue"><strong>💬 ChatGPT = Probabilistic Token Engine</strong>Not "thinking" — predicting the most likely next token based on training data. Temperature=0 → deterministic. Temperature=1 → creative.</div>
  <div class="concept c-green"><strong>🎭 System vs User Role</strong>System prompt = contract/rules the model must follow. User = runtime message. Agent behavior is defined in System.</div>
  <div class="concept c-orange"><strong>🔌 OpenAI API Pattern</strong>REST call → JSON payload → JSON response. Same pattern as calling any microservice. Simple but powerful.</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: Your First Production-Grade LLM Call</div>
<pre><span class="kw">import</span> os
<span class="kw">from</span> openai <span class="kw">import</span> OpenAI

client = OpenAI(api_key=os.environ[<span class="st">"OPENAI_API_KEY"</span>])

<span class="cm"># ARCHITECT DECISION: Always pass system role first to define agent behavior contract</span>
<span class="cm"># Temperature 0.1 for structured tasks, 0.7 for creative tasks</span>
response = client.chat.completions.create(
    model=<span class="st">"gpt-4o-mini"</span>,
    temperature=<span class="nm">0.1</span>,       <span class="cm"># near-deterministic for tool calls</span>
    max_tokens=<span class="nm">500</span>,        <span class="cm"># always cap to control costs</span>
    messages=[
        {<span class="st">"role"</span>: <span class="st">"system"</span>, <span class="st">"content"</span>: <span class="st">"You are a precise banking assistant. Answer only from provided context."</span>},
        {<span class="st">"role"</span>: <span class="st">"user"</span>, <span class="st">"content"</span>: <span class="st">"What is the current fixed deposit rate?"</span>}
    ]
)
answer = response.choices[<span class="nm">0</span>].message.content
tokens_used = response.usage.total_tokens  <span class="cm"># always log this!</span></pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A</div>
<div class="qa"><div class="q">Q: What is the difference between temperature=0 and temperature=1 in production agents?</div>
<div class="a">A: temperature=0 makes the model deterministic (always picks highest probability token) — use for tool-calling, JSON generation, math. temperature=1 samples from the full distribution — use for creative text. Production agents use 0.1 for reliability.</div></div>
<div class="qa"><div class="q">Q: How do you prevent prompt injection in a banking chatbot?</div>
<div class="a">A: Pre-execution lexical firewall (regex scan for "ignore previous instructions") BEFORE the LLM call. The system prompt alone is NOT sufficient — models can be jailbroken.</div></div>
</div>
<div class="architect">
<div class="atitle">👑 ARCHITECT THINKING: How I Design Every LLM Integration</div>
<ul><li>First question: "Does this NEED an LLM, or can a regex/database query solve it?" Use LLMs only where natural language understanding is required.</li>
<li>Always externalize: API key → env var, model name → config, system prompt → file. Never hardcode.</li>
<li>Cost = tokens × price/token. Design token budgets before writing code. A chat UI costs ~$2/1000 sessions at 4o-mini rates.</li></ul>
</div>
</div>
</div>

<!-- WEEK 2 -->
<div class="week">
<div class="week-header w2"><span class="week-num">Week 2</span> Python: Data Types, Functions & Control Flow</div>
<div class="week-body">
<div class="summary">🟠 Python's dynamic typing, list comprehensions, and decorators are the building blocks of LangChain tools and agent pipelines. Master these to write clean, testable agentic code.</div>
<div class="grid2">
  <div class="concept c-orange"><strong>📦 Dicts & Dataclasses</strong>Agent state, tool schemas, and API payloads are all dicts. Pydantic models add type safety — use them for all tool inputs.</div>
  <div class="concept c-blue"><strong>🔁 Exception Handling in AI</strong>LLM APIs fail (rate limits, timeouts). Every LLM call needs try/except with retry logic and circuit breaker.</div>
  <div class="concept c-green"><strong>🎯 Decorators = Tool Wrappers</strong><code>@tool</code> in LangChain is a Python decorator. Understanding decorators = understanding how tool registration works internally.</div>
  <div class="concept c-purple"><strong>🔄 Generator Patterns</strong>Streaming LLM responses use Python generators. <code>for chunk in stream: yield chunk</code> — critical for real-time chat UIs.</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: Writing a Safe LangChain Tool</div>
<pre><span class="kw">from</span> langchain_core.tools <span class="kw">import</span> tool
<span class="kw">from</span> pydantic <span class="kw">import</span> BaseModel, Field

<span class="kw">class</span> <span class="fn">LoanInput</span>(BaseModel):
    principal: float = Field(..., gt=<span class="nm">0</span>, description=<span class="st">"Loan amount in INR"</span>)
    tenure_months: int = Field(..., gt=<span class="nm">0</span>, le=<span class="nm">360</span>)

<span class="nm">@tool</span>(args_schema=LoanInput)
<span class="kw">def</span> <span class="fn">calculate_emi</span>(principal: float, tenure_months: int) -> dict:
    <span class="st">"""Calculate monthly EMI for a loan. Use this when user asks about loan repayment."""</span>
    rate = <span class="nm">0.00875</span>  <span class="cm"># 10.5% annual / 12</span>
    factor = (<span class="nm">1</span> + rate) ** tenure_months
    emi = (principal * rate * factor) / (factor - <span class="nm">1</span>)
    <span class="kw">return</span> {<span class="st">"monthly_emi"</span>: <span class="fn">round</span>(emi, <span class="nm">2</span>), <span class="st">"total_payment"</span>: <span class="fn">round</span>(emi * tenure_months, <span class="nm">2</span>)}
<span class="cm"># The docstring IS the tool description — write it like a prompt for the agent!</span></pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A</div>
<div class="qa"><div class="q">Q: Why must all LangChain tool inputs use Pydantic models?</div>
<div class="a">A: LLMs emit JSON with loose types — strings instead of ints, nulls where values are expected. Pydantic validates and coerces at the boundary, preventing TypeErrors deep inside the tool execution. It's the contract between probabilistic LLM output and deterministic Python code.</div></div>
</div>
<div class="tip"><span class="icon">💡</span>Java Parallel: <code>@tool</code> decorator = Spring <code>@RestController</code> method registration. The docstring = the OpenAPI spec description that the LLM uses to decide when to call this tool.</div>
</div>
</div>

<!-- WEEK 3 -->
<div class="week">
<div class="week-header w3"><span class="week-num">Week 3</span> Working with Libraries: NumPy, Pandas, Matplotlib</div>
<div class="week-body">
<div class="summary">🟢 NumPy arrays ARE embeddings. Pandas DataFrames are how you load, clean, and feed data to agents. Matplotlib visualizes similarity scores and model behavior for debugging and evaluation reports.</div>
<div class="grid3">
  <div class="concept c-green"><strong>🔢 NumPy</strong>Vectorized math on float32 arrays. Cosine similarity computation. Embedding manipulations done here.</div>
  <div class="concept c-blue"><strong>🐼 Pandas</strong>Load CSVs → feed as tool context. DataFrame = structured knowledge base for a tabular-data agent.</div>
  <div class="concept c-orange"><strong>📊 Matplotlib</strong>Plot token usage, similarity distributions, evaluation scores. Essential for reporting to stakeholders.</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: Build a Mini Embedding Similarity Inspector</div>
<pre><span class="kw">import</span> numpy <span class="kw">as</span> np
<span class="kw">from</span> openai <span class="kw">import</span> OpenAI
client = OpenAI()

<span class="kw">def</span> <span class="fn">get_embedding</span>(text): 
    <span class="kw">return</span> np.array(client.embeddings.create(input=text, model=<span class="st">"text-embedding-3-small"</span>).data[<span class="nm">0</span>].embedding)

<span class="kw">def</span> <span class="fn">cosine_similarity</span>(a, b): 
    <span class="kw">return</span> np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

<span class="cm"># ARCHITECT USE CASE: Debug why RAG retrieved wrong chunks</span>
query = get_embedding(<span class="st">"What is the return policy for electronics?"</span>)
chunk1 = get_embedding(<span class="st">"Electronics have a 15-day return window."</span>)
chunk2 = get_embedding(<span class="st">"Prime membership costs INR 999/year."</span>)
print(f<span class="st">"Correct chunk similarity: {cosine_similarity(query, chunk1):.4f}"</span>)  <span class="cm"># ~0.88</span>
print(f<span class="st">"Wrong chunk similarity: {cosine_similarity(query, chunk2):.4f}"</span>)    <span class="cm"># ~0.42</span></pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A</div>
<div class="qa"><div class="q">Q: A RAG chatbot is retrieving irrelevant chunks. How do you debug it?</div>
<div class="a">A: (1) Compute cosine similarity between query embedding and all stored chunk embeddings. (2) If correct chunk similarity &lt; 0.7, the chunk text or query is too different semantically — improve chunking strategy. (3) If correct chunk similarity is high but still not returned, check if k (top-k) is too small or cosine threshold is too strict. (4) Visualize with Matplotlib histogram of all chunk similarities to find the right threshold.</div></div>
</div>
</div>
</div>

<!-- WEEK 4 -->
<div class="week">
<div class="week-header w4"><span class="week-num">Week 4</span> Fundamentals of AI & Machine Learning</div>
<div class="week-body">
<div class="summary">🔵 ML is pattern extraction from data. Transformers are deep supervised learners. RLHF is how GPT models are aligned to human preferences. Understanding this lets you debug model behavior, choose the right model, and justify design decisions.</div>
<div class="grid2">
  <div class="concept c-blue"><strong>📚 Supervised Learning</strong>Labelled data → model learns mapping. LLMs are trained this way: next-token prediction on trillions of labelled (token, next-token) pairs.</div>
  <div class="concept c-green"><strong>🎮 Reinforcement Learning (RLHF)</strong>Human rates outputs → Reward Model trained → LLM fine-tuned with PPO to maximize reward. This is WHY GPT is helpful and refuses harmful requests.</div>
  <div class="concept c-orange"><strong>📈 Overfitting in Prompts</strong>Over-specifying examples makes LLM memorize format, not generalize. Too few examples = poor adherence. Balance with 3–5 few-shot examples.</div>
  <div class="concept c-red"><strong>🧠 Transfer Learning</strong>Foundation model pre-trained on internet → fine-tuned on domain data. Like a new Java dev who knows Spring Boot but needs to learn your domain.</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: Evaluate if You Need Fine-Tuning vs RAG (Decision Framework)</div>
<pre><span class="cm"># ARCHITECT DECISION TREE — Use this before starting any AI project:</span>
<span class="cm">#</span>
<span class="cm"># Q1: Does the model need DOMAIN KNOWLEDGE (facts, documents, policies)?</span>
<span class="cm">#     YES → Use RAG (cheaper, updatable, traceable)</span>
<span class="cm">#     NO  → Continue below</span>
<span class="cm">#</span>
<span class="cm"># Q2: Does the model need to BEHAVE differently (tone, format, persona)?</span>
<span class="cm">#     YES → Use Fine-Tuning (expensive but effective)</span>
<span class="cm">#     NO  → Use Prompt Engineering (start here ALWAYS)</span>
<span class="cm">#</span>
<span class="cm"># Q3: Do you need to improve on COMPLEX REASONING tasks?</span>
<span class="cm">#     YES → Use Chain-of-Thought prompting + GPT-4 class model</span>
<span class="cm">#     NO  → GPT-4o-mini is usually sufficient</span>
<span class="cm">#</span>
<span class="cm"># RULE: Always try Prompt Engineering → RAG → Fine-Tuning (in that order)</span>
<span class="cm"># Fine-tuning costs $1,000+ and takes weeks. RAG takes 2 days.</span></pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A</div>
<div class="qa"><div class="q">Q: Your client says "Can we fine-tune GPT on our company data?" What is your response as an AI architect?</div>
<div class="a">A: "Let's first understand what problem we're solving. If the issue is the model doesn't know our company's FACTS (policies, products, procedures) — RAG is the right solution: cheaper, faster, and the knowledge is auditable and updatable in real-time. Fine-tuning is appropriate when we need to change HOW the model behaves — its tone, format, or domain-specific reasoning style — and we have 1,000+ high-quality labelled examples. What specifically is the model getting wrong today?"</div></div>
</div>
<div class="architect">
<div class="atitle">👑 ARCHITECT THINKING: The ML Mental Model</div>
<ul><li>Every ML system is: Data Quality × Model Capacity × Training Compute = Performance. Fix data first, always.</li>
<li>When a model "hallucinates", it's not broken — it's doing exactly what it was trained to do (predict probable text). Fix: constrain it with RAG + strict system prompt + output validation.</li>
<li>For 90% of enterprise use cases: GPT-4o-mini + RAG + good prompting outperforms a custom fine-tuned model at 1/100th the cost.</li></ul>
</div>
</div>
</div>

<!-- WEEK 5 -->
<div class="week">
<div class="week-header w5"><span class="week-num">Week 5</span> Large Language Models — Deep Dive</div>
<div class="week-body">
<div class="summary">🟣 The Transformer attention mechanism is the engine of all modern AI. Understanding it lets you debug context length issues, choose the right model for a task, and explain AI behavior to non-technical stakeholders.</div>
<div class="grid2">
  <div class="concept c-purple"><strong>⚡ Self-Attention Formula</strong>Attention(Q,K,V) = softmax(QKᵀ/√d_k)×V. Query = "what am I looking for?" Key = "what do I contain?" Value = "what I give you."</div>
  <div class="concept c-blue"><strong>🌡️ Temperature & Sampling</strong>t=0.1: structured output (JSON, code). t=0.7: natural conversation. t=1.5: creative writing. Never use t>1.0 in production agents.</div>
  <div class="concept c-green"><strong>🪟 Context Window Strategy</strong>128k tokens ≠ free. Cost scales with context. For agents: system prompt (500) + history (1000) + retrieved context (2000) + response (500) = budget carefully.</div>
  <div class="concept c-orange"><strong>📝 BPE Tokenization Impact</strong>"Mumbai" = 1 token. "Thiruvananthapuram" = 5 tokens. Rare/domain words cost more tokens. Design prompts with common vocabulary.</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: Production Token Budget Calculator</div>
<pre><span class="kw">def</span> <span class="fn">calculate_session_cost</span>(system_prompt: str, history_turns: int, context_chunks: int) -> dict:
    <span class="cm">"""Architect tool: estimate session cost before deployment"""</span>
    tokens = {
        <span class="st">"system_prompt"</span>: len(system_prompt) // <span class="nm">4</span>,      <span class="cm"># ~4 chars per token</span>
        <span class="st">"conversation_history"</span>: history_turns * <span class="nm">150</span>,     <span class="cm"># avg 150 tokens per turn</span>
        <span class="st">"retrieved_context"</span>: context_chunks * <span class="nm">200</span>,       <span class="cm"># 200 token chunks</span>
        <span class="st">"response_output"</span>: <span class="nm">300</span>                            <span class="cm"># typical response</span>
    }
    total = sum(tokens.values())
    cost_usd = total * <span class="nm">0.00000015</span>  <span class="cm"># gpt-4o-mini: $0.15 per 1M tokens</span>
    <span class="kw">return</span> {<span class="st">"total_tokens"</span>: total, <span class="st">"cost_per_session_usd"</span>: f<span class="st">"${cost_usd:.6f}"</span>,
            <span class="st">"monthly_cost_1000_users"</span>: f<span class="st">"${cost_usd * 1000 * 30:.2f}"</span>}
<span class="cm"># Output: {'total_tokens': 1100, 'cost_per_session': '$0.000165', 'monthly': '$4.95'}</span></pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A</div>
<div class="qa"><div class="q">Q: Explain the attention mechanism to a non-technical product manager.</div>
<div class="a">A: "Imagine you're reading the sentence 'The bank refused the loan because it was risky.' The word 'it' could mean the bank or the loan. Human brains compute attention — you subconsciously weigh the relationship between 'it' and every other word. The transformer does exactly this mathematically: for every word, it computes a weighted relationship score with every other word in the entire input, enabling it to understand context, pronouns, and long-range dependencies."</div></div>
<div class="qa"><div class="q">Q: Why does RAG outperform fine-tuning for knowledge-intensive tasks?</div>
<div class="a">A: Fine-tuning bakes knowledge into model weights — but weights can't be updated without expensive retraining. RAG retrieves fresh knowledge at inference time from an external database that can be updated in seconds. For dynamic business data (prices, policies, inventory), RAG is the only practical approach.</div></div>
</div>
</div>
</div>

<!-- WEEK 6 -->
<div class="week">
<div class="week-header w6"><span class="week-num">Week 6</span> Embedding Models & Vector Databases</div>
<div class="week-body">
<div class="summary">💗 Embeddings are the mathematical bridge between human language and machine search. A vector database stores these embeddings for fast similarity retrieval. This is the core technology behind every RAG chatbot, semantic search engine, and recommendation system.</div>
<div class="grid2">
  <div class="concept c-pink"><strong>🧮 Embedding Model Choices</strong>OpenAI text-embedding-3-small (1536-dim, $0.02/1M tokens). Local: sentence-transformers/all-MiniLM-L6-v2 (384-dim, FREE). Choose based on accuracy vs. cost.</div>
  <div class="concept c-blue"><strong>🗄️ Vector DB Comparison</strong>FAISS: local, fast, no server. Chroma: local, persistent. Pinecone: cloud, scalable. Weaviate: hybrid search. Start with FAISS for prototypes.</div>
  <div class="concept c-green"><strong>📐 Distance Metrics</strong>Cosine: measures angle (best for text). Euclidean: measures absolute distance. Dot product: fastest but biased by vector magnitude.</div>
  <div class="concept c-orange"><strong>⚙️ Index Types</strong>Flat (brute force, exact, slow for &gt;100k vectors). HNSW (approximate, fast, scalable to billions). IVF (partitioned, good middle ground).</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: Build a Complete Document Search System</div>
<pre><span class="kw">from</span> langchain_openai <span class="kw">import</span> OpenAIEmbeddings
<span class="kw">from</span> langchain_community.vectorstores <span class="kw">import</span> FAISS
<span class="kw">from</span> langchain.text_splitter <span class="kw">import</span> RecursiveCharacterTextSplitter
<span class="kw">from</span> langchain_community.document_loaders <span class="kw">import</span> TextLoader

<span class="cm"># STEP 1: Load and chunk documents</span>
loader = TextLoader(<span class="st">"company_policies.txt"</span>)
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(
    chunk_size=<span class="nm">800</span>,       <span class="cm"># optimal: captures full paragraphs</span>
    chunk_overlap=<span class="nm">150</span>,   <span class="cm"># overlap prevents losing context at boundaries</span>
    separators=[<span class="st">"\n\n"</span>, <span class="st">"\n"</span>, <span class="st">" "</span>]  <span class="cm"># try paragraph breaks first</span>
)
chunks = splitter.split_documents(docs)

<span class="cm"># STEP 2: Embed and index</span>
embeddings = OpenAIEmbeddings(model=<span class="st">"text-embedding-3-small"</span>)
vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local(<span class="st">"./vectorstore"</span>)  <span class="cm"># persist to disk</span>

<span class="cm"># STEP 3: Retrieve similar chunks</span>
results = vectorstore.similarity_search_with_score(<span class="st">"return policy electronics"</span>, k=<span class="nm">3</span>)
<span class="kw">for</span> doc, score <span class="kw">in</span> results:
    print(f<span class="st">"Score: {score:.3f} | Source: {doc.metadata['source']}"</span>)
    <span class="cm"># Score < 1.15 = good match. > 1.5 = poor match (cosine distance)</span></pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A</div>
<div class="qa"><div class="q">Q: How do you choose chunk size for a RAG system?</div>
<div class="a">A: Rule of thumb: 800–1000 characters (200–250 tokens) for policy/documentation text. Smaller (400–600) for precise Q&A. Larger (1200–1500) for narrative documents where context matters. Always maintain 15–20% overlap to avoid cutting sentences at boundaries. Test by running 20 representative queries and checking if the correct chunk is in top-3 results.</div></div>
</div>
</div>
</div>

<h3 class="section">🤖 PART B: Agentic Architectures & Frameworks (Weeks 7–12)</h3>

<!-- WEEK 7 -->
<div class="week">
<div class="week-header w7"><span class="week-num">Week 7</span> Agentic Tools in Python — LangChain Deep Dive</div>
<div class="week-body">
<div class="summary">🔵 LangChain LCEL (Expression Language) uses functional composition with the pipe operator to build declarative, asynchronous, streamable AI pipelines. Understanding LCEL is understanding how modern AI backends are architected.</div>
<div class="grid2">
  <div class="concept c-blue"><strong>🔗 LCEL Pipe Composition</strong><code>chain = prompt | llm | parser</code>. Each component is a Runnable. Supports batch, stream, async natively. No boilerplate.</div>
  <div class="concept c-green"><strong>🛠️ Tool Binding</strong><code>llm_with_tools = llm.bind_tools([tool1, tool2])</code>. LLM decides WHEN to call which tool based on docstring + schema.</div>
  <div class="concept c-orange"><strong>💬 Prompt Templates</strong>Variables injected at runtime: <code>{user_name}</code>, <code>{context}</code>. Enables dynamic, personalized agent behavior.</div>
  <div class="concept c-purple"><strong>🔄 Streaming Responses</strong><code>async for chunk in chain.astream(input): yield chunk</code>. Essential for real-time chat UIs. Reduces perceived latency.</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: Complete ReAct Agent with LangChain</div>
<pre><span class="kw">from</span> langchain_openai <span class="kw">import</span> ChatOpenAI
<span class="kw">from</span> langchain.agents <span class="kw">import</span> create_react_agent, AgentExecutor
<span class="kw">from</span> langchain_core.prompts <span class="kw">import</span> ChatPromptTemplate
<span class="kw">from</span> langchain_core.tools <span class="kw">import</span> tool
<span class="kw">import</span> asyncio

<span class="nm">@tool</span>
<span class="kw">def</span> <span class="fn">get_account_balance</span>(account_id: str) -> str:
    <span class="st">"""Fetch current balance for a bank account. Use when user asks about balance."""</span>
    <span class="kw">return</span> f<span class="st">"Account {account_id}: Balance INR 1,45,230.50, Last transaction: Salary credit"</span>

<span class="nm">@tool</span>
<span class="kw">def</span> <span class="fn">get_loan_offers</span>(credit_score: int) -> str:
    <span class="st">"""Get available loan offers based on credit score."""</span>
    <span class="kw">if</span> credit_score >= <span class="nm">750</span>: <span class="kw">return</span> <span class="st">"Eligible: Personal Loan 10.5%, Home Loan 8.5%"</span>
    <span class="kw">return</span> <span class="st">"Limited options. Credit score improvement recommended first."</span>

llm = ChatOpenAI(model=<span class="st">"gpt-4o-mini"</span>, temperature=<span class="nm">0.1</span>)
agent = create_react_agent(llm, [get_account_balance, get_loan_offers], 
                           ChatPromptTemplate.from_messages([
                               (<span class="st">"system"</span>, <span class="st">"You are a helpful banking assistant. {agent_scratchpad}"</span>),
                               (<span class="st">"human"</span>, <span class="st">"{input}"</span>)]))
executor = AgentExecutor(agent=agent, tools=[get_account_balance, get_loan_offers],
                         max_iterations=<span class="nm">5</span>, verbose=<span class="kw">True</span>)  <span class="cm"># ALWAYS set max_iterations!</span>
result = executor.invoke({<span class="st">"input"</span>: <span class="st">"What's the balance in account ACC123 and am I eligible for a loan with score 780?"</span>})</pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A</div>
<div class="qa"><div class="q">Q: What happens if you don't set max_iterations in an AgentExecutor?</div>
<div class="a">A: The agent can loop indefinitely. If a tool always returns an error or the LLM gets confused, it enters an infinite Thought→Action→Observation loop consuming tokens and time until the API rate limit kills it. Always set max_iterations=5 to 10, and max_execution_time for wall-clock protection.</div></div>
</div>
<div class="architect">
<div class="atitle">👑 ARCHITECT THINKING: Designing Tool Docstrings</div>
<ul><li>The tool docstring IS the specification the LLM uses to decide when to call the tool. Write it like a precise API spec: what it does, when to use it, what it needs, what it returns.</li>
<li>Bad: <code>"""Get data."""</code> — the LLM won't know when to use this.</li>
<li>Good: <code>"""Fetch current account balance from CBS. Use when user asks about balance, available funds, or account status. Requires account_id parameter."""</code></li></ul>
</div>
</div>
</div>

<!-- WEEK 8 -->
<div class="week">
<div class="week-header w8"><span class="week-num">Week 8</span> Introduction to Agentic AI</div>
<div class="week-body">
<div class="summary">🟠 An agent is an LLM wrapped in a Perception-Planning-Action-Observation loop with tools and memory. Understanding agent autonomy levels helps you choose the right architecture for each business requirement.</div>
<div class="grid2">
  <div class="concept c-orange"><strong>🤖 Agent = LLM + Tools + Memory + Goal</strong>Remove any of these and it's no longer an agent. The loop runs until the goal is achieved or a stopping condition fires.</div>
  <div class="concept c-blue"><strong>📊 4 Autonomy Levels</strong>L1: Hardcoded (regex chatbot). L2: Prompt-driven (no tools). L3: Tool-using (ReAct). L4: Self-improving (RL feedback loop).</div>
  <div class="concept c-green"><strong>🔄 The ReAct Loop</strong>Thought: "I need to check the balance" → Action: call_tool(get_balance) → Observation: "INR 50,000" → Thought: "Now I can answer" → Final Answer.</div>
  <div class="concept c-red"><strong>⚠️ When NOT to Use Agents</strong>Simple CRUD operations, fixed-format reports, rule-based routing. Agents add latency (2–5s) and cost. Use only when reasoning over variable inputs is needed.</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: Agent vs Non-Agent Decision Matrix (Real Project)</div>
<pre><span class="cm">"""
REAL PROJECT SCENARIO: Bank Customer Support Automation
Team asks: "Should everything be an agent?"

DECISION ANALYSIS:
Task 1: "What's my balance?" -> L2 chatbot or direct API call (NOT an agent)
  - Fixed query pattern, deterministic, no reasoning needed
  - Agent adds 2s latency and $0.002 per call unnecessarily

Task 2: "Should I invest my savings in FD or MF given my profile?" → L3 AGENT
  - Needs tools: get_profile, get_market_data, get_fd_rates, calculate_returns
  - Needs reasoning: compare options, weigh risk tolerance, personalize recommendation
  - Reasoning across multiple tool outputs = agent territory

Task 3: "Process monthly salary crediting for 10,000 employees" → BATCH JOB, NOT AGENT
  - Deterministic, high-volume, no natural language reasoning needed
  - Use Spring Batch / Python Celery, not LangChain

ARCHITECT RULE: If a 5-line if/else statement can solve it, don't build an agent.
"""</span></pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A</div>
<div class="qa"><div class="q">Q: Design an AI customer support system for a bank. Walk me through your architecture.</div>
<div class="a">A: I'd use a 3-tier approach. Tier 1: Intent classifier (LLM with temperature=0) routes to specialized agents. Tier 2: Task-specific L3 agents (balance agent, loan agent, complaint agent) — each with 3–5 tools specific to their domain. Tier 3: Safety layer — pre-execution guardrail blocks transactional mutations, post-execution PII scrubber before logging. Memory: ConversationBufferWindowMemory(k=5) for context, FAISS vectorstore for policy RAG. Framework: LangChain for single-agent tasks, CrewAI for multi-step investigations.</div></div>
</div>
</div>
</div>

<!-- WEEK 9 -->
<div class="week">
<div class="week-header w9"><span class="week-num">Week 9</span> Programming Frameworks for Agentic Systems</div>
<div class="week-body">
<div class="summary">🟢 Choosing the wrong framework costs weeks of refactoring. Match framework to use case: LangChain for RAG/tool chains, CrewAI for role-based teams, AutoGen for LLM-driven code generation, DSPy when you need prompt optimization at scale.</div>
<div class="grid3">
  <div class="concept c-green"><strong>🔗 LangChain LCEL</strong>Universal Swiss army knife. Largest ecosystem. Best RAG + tool chain support. Use when you need maximum flexibility.</div>
  <div class="concept c-blue"><strong>⚓ CrewAI</strong>Opinionated multi-agent. Role → Task → Crew. Sequential or hierarchical. Best for: research teams, writing pipelines, analysis workflows.</div>
  <div class="concept c-orange"><strong>🤝 AutoGen</strong>MS Research. Multi-turn LLM conversations + code execution. Best for: iterative code writing, adversarial debate, complex problem solving with code.</div>
  <div class="concept c-purple"><strong>🧠 DSPy</strong>Treats prompts as programs. Compiles and optimizes instructions automatically using training examples. Use when prompt quality matters at scale.</div>
  <div class="concept c-red"><strong>🏢 Semantic Kernel</strong>Enterprise SDK. Strong .NET/Java support. Azure-native. Best for large enterprises with existing Microsoft stack.</div>
  <div class="concept c-teal"><strong>🌾 Haystack</strong>NLP document pipeline specialist. Production-grade retrieval, ranking, and reader components. Best for search-heavy applications.</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: CrewAI Research & Report Team</div>
<pre><span class="kw">from</span> crewai <span class="kw">import</span> Agent, Task, Crew, Process
<span class="kw">from</span> langchain_openai <span class="kw">import</span> ChatOpenAI

llm = ChatOpenAI(model=<span class="st">"gpt-4o-mini"</span>, temperature=<span class="nm">0.1</span>)

researcher = Agent(role=<span class="st">"Senior Market Research Analyst"</span>,
    goal=<span class="st">"Research and gather comprehensive data on given topic"</span>,
    backstory=<span class="st">"10 years in financial market research. Expert at identifying key trends."</span>,
    llm=llm, allow_delegation=<span class="kw">False</span>,  <span class="cm"># CRITICAL: prevents circular delegation</span>
    verbose=<span class="kw">True</span>)

writer = Agent(role=<span class="st">"Executive Report Writer"</span>,
    goal=<span class="st">"Transform research into clear, actionable executive summaries"</span>,
    backstory=<span class="st">"Former investment banker. Writes reports that drive decisions."</span>,
    llm=llm, allow_delegation=<span class="kw">False</span>)

research_task = Task(description=<span class="st">"Analyze key trends in Indian fintech sector 2025"</span>,
    expected_output=<span class="st">"Bullet-point research with 5 key findings and supporting data"</span>,
    agent=researcher)

write_task = Task(description=<span class="st">"Write 1-page executive summary from the research provided"</span>,
    expected_output=<span class="st">"Professional executive summary with recommendations"</span>,
    agent=writer, context=[research_task])  <span class="cm"># receives researcher output</span>

crew = Crew(agents=[researcher, writer], tasks=[research_task, write_task],
            process=Process.sequential, verbose=<span class="kw">True</span>)
result = crew.kickoff()</pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A</div>
<div class="qa"><div class="q">Q: When would you choose AutoGen over CrewAI?</div>
<div class="a">A: AutoGen when: (1) agents need to write, execute, and debug code iteratively, (2) you need adversarial debate patterns where one agent critiques another's work in natural dialogue, (3) you need human-in-the-loop with UserProxyAgent for approval gates. CrewAI when: (1) you need structured role-based pipelines with clear task handoffs, (2) sequential or hierarchical execution with predefined roles, (3) non-code workflows like research → writing → review.</div></div>
</div>
</div>
</div>

<!-- WEEK 10 -->
<div class="week">
<div class="week-header w10"><span class="week-num">Week 10</span> Agent Architectures & Multi-Agent Collaboration</div>
<div class="week-body">
<div class="summary">🟣 The choice of agent architecture (reactive vs deliberative vs BDI) determines reliability, explainability, and performance. Multi-agent patterns solve problems no single agent can — but introduce coordination complexity that must be explicitly managed.</div>
<div class="grid2">
  <div class="concept c-purple"><strong>⚡ Reactive Architecture</strong>Stimulus → Response. No internal model. Ultra-fast. Use for: alert systems, simple routing, high-frequency event processing.</div>
  <div class="concept c-blue"><strong>🗺️ Deliberative (ReAct)</strong>Reason then act. Maintains internal world model. Slower but explainable. Use for: complex analysis, multi-step decisions, audit-required workflows.</div>
  <div class="concept c-green"><strong>🤝 Cooperative Pattern</strong>Agents share a goal, divide complementary tasks. Researcher + Writer + Reviewer crew. Output quality = sum of specializations.</div>
  <div class="concept c-red"><strong>🏆 Adversarial/Debate Pattern</strong>Agent A proposes → Agent B critiques → Synthesizer resolves. Used in: code review agents, medical second-opinion systems, financial risk assessment.</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: Adversarial Debate Pattern for Code Review</div>
<pre><span class="cm"># REAL USE CASE: Automated PR Code Review System</span>
<span class="cm"># Pattern: Developer Agent writes code → Security Agent attacks it → Architect resolves</span>

developer_agent = Agent(role=<span class="st">"Senior Backend Developer"</span>,
    goal=<span class="st">"Write clean, efficient Python code for given requirements"</span>,
    backstory=<span class="st">"10yr Java dev transitioning to Python. Strong in algorithms, learning security."</span>,
    allow_delegation=<span class="kw">False</span>)

security_agent = Agent(role=<span class="st">"Application Security Engineer"</span>,
    goal=<span class="st">"Find every security vulnerability in provided code. Be thorough and adversarial."</span>,
    backstory=<span class="st">"OWASP expert. Found 200+ CVEs. Cynical about developer security practices."</span>,
    allow_delegation=<span class="kw">False</span>)

architect_agent = Agent(role=<span class="st">"Principal Software Architect"</span>,
    goal=<span class="st">"Resolve security concerns pragmatically. Approve or reject the code with reasoning."</span>,
    backstory=<span class="st">"20yr experience. Balances security with delivery velocity."</span>,
    allow_delegation=<span class="kw">False</span>)

<span class="cm"># Tasks flow: code → attack → resolve (sequential, no delegation between peers)</span>
<span class="cm"># This pattern catches 3x more security issues than single-agent review</span></pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A</div>
<div class="qa"><div class="q">Q: How do you prevent circular delegation in a multi-agent system?</div>
<div class="a">A: (1) Set <code>allow_delegation=False</code> on all agents in sequential pipelines — agents can only complete their assigned tasks. (2) Use Process.hierarchical with a dedicated manager_llm that has delegation authority — non-manager agents cannot delegate. (3) Implement a session-level iteration counter — if agent X calls agent Y more than 3 times, raise DelegationLimitException. (4) Add a token budget tripwire — if session exceeds 4k tokens, abort and escalate to human.</div></div>
</div>
</div>
</div>

<!-- WEEK 11 -->
<div class="week">
<div class="week-header w11"><span class="week-num">Week 11</span> Decision Making & Planning in Agents</div>
<div class="week-body">
<div class="summary">💡 ReAct (Reason + Act) is the dominant production planning pattern because it's explainable, debuggable, and naturally handles tool selection. Chain-of-Thought prompting dramatically improves multi-step reasoning accuracy on complex business problems.</div>
<div class="grid2">
  <div class="concept c-red"><strong>⚡ ReAct Step-by-Step</strong>Thought → Action → Observation → Thought → ... → Final Answer. Each step is logged. Regulators can audit WHY the agent made each decision.</div>
  <div class="concept c-blue"><strong>🌲 Task Decomposition</strong>Complex goal → DAG of sub-tasks. Like breaking a Spring Batch job into steps. Each sub-task has a clear input, tool, and expected output.</div>
  <div class="concept c-green"><strong>🔗 Chain of Thought (CoT)</strong>"Think step by step" prefix. Forces intermediate reasoning before answer. Reduces math/logic errors by 40–60%. Essential for financial calculations.</div>
  <div class="concept c-orange"><strong>🎯 Plan and Execute Pattern</strong>Planner LLM creates the plan → Executor LLM executes each step. Separation enables planning with expensive model, execution with cheap model.</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: Plan-and-Execute Financial Analysis Agent</div>
<pre><span class="cm"># REAL PROJECT: Automated Investment Portfolio Analyzer</span>
<span class="cm"># Complex multi-step reasoning: user query → plan → execute → synthesize</span>

system_prompt = <span class="st">"""You are a financial planning AI. For every complex analysis:

STEP 1 - PLAN: Break the task into numbered sub-steps before starting.
Example for "Analyze my portfolio risk":
  Plan:
  1. Fetch all current holdings using get_portfolio tool
  2. Get current market prices for each holding
  3. Calculate portfolio allocation percentages
  4. Assess risk using Sharpe ratio and max drawdown
  5. Compare against user's stated risk appetite
  6. Generate recommendation

STEP 2 - EXECUTE: Follow the plan using available tools.
STEP 3 - VERIFY: Check if each step's output is reasonable before proceeding.
STEP 4 - SYNTHESIZE: Combine all observations into a coherent recommendation.

NEVER calculate numbers yourself. ALWAYS use deterministic tools for math."""</span>

<span class="cm"># WHY THIS WORKS: Forces structured reasoning, prevents hallucinated calculations,</span>
<span class="cm"># creates auditable decision trail for compliance requirements</span></pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A</div>
<div class="qa"><div class="q">Q: How do you handle an agent that gets "stuck" in a reasoning loop?</div>
<div class="a">A: Defense-in-depth: (1) max_iterations=5 in AgentExecutor — hard iteration cap. (2) max_execution_time=30 — wall-clock timeout. (3) Inject intermediate checkpoints: if Observation contains "Error" 3 times consecutively, trigger human escalation. (4) Circuit breaker pattern: if total session tokens exceeds budget, raise exception and return graceful fallback. (5) Log all intermediate steps — replay to identify where reasoning diverged.</div></div>
</div>
</div>
</div>

<!-- WEEK 12 -->
<div class="week">
<div class="week-header w12"><span class="week-num">Week 12</span> Memory & Knowledge Retrieval + Model Context Protocol (MCP)</div>
<div class="week-body">
<div class="summary">🔵 Memory is what transforms a one-shot LLM into a contextually aware conversational agent. MCP (Anthropic, Nov 2024) is the universal "USB-C" for AI tools — any agent, any tool, one standardized interface over JSON-RPC 2.0.</div>
<div class="grid2">
  <div class="concept c-blue"><strong>🧠 Memory Architecture</strong>Working Memory (context window, 128k tokens, ephemeral) + Episodic Memory (conversation history, compressed) + Semantic Memory (vector store, persistent).</div>
  <div class="concept c-green"><strong>💾 ConversationSummaryBufferMemory</strong>Best production memory: keeps last k turns verbatim (for immediate context) + LLM-compressed summary of older turns. Prevents context overflow.</div>
  <div class="concept c-orange"><strong>📡 MCP Architecture</strong>Client (Agent) → JSON-RPC 2.0 → Server (Tool). Server exposes: tools/list (discover), tools/call (execute). Agent never talks to databases directly.</div>
  <div class="concept c-purple"><strong>🔌 MCP Transport Options</strong>stdio: local process (secure, for local tools). HTTP+SSE: remote server (for cloud tools, databases, APIs). Agent connects to multiple MCP servers simultaneously.</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: Full Memory + MCP Integration</div>
<pre><span class="kw">from</span> langchain.memory <span class="kw">import</span> ConversationSummaryBufferMemory
<span class="kw">from</span> langchain_openai <span class="kw">import</span> ChatOpenAI
<span class="kw">from</span> langchain.chains <span class="kw">import</span> ConversationChain

llm = ChatOpenAI(model=<span class="st">"gpt-4o-mini"</span>, temperature=<span class="nm">0.1</span>)

<span class="cm"># SummaryBufferMemory: verbatim for recent turns, summarized for older ones</span>
memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=<span class="nm">1000</span>,  <span class="cm"># beyond 1000 tokens → auto-summarize older turns</span>
    return_messages=<span class="kw">True</span>   <span class="cm"># return as message objects for ChatPromptTemplate</span>
)

<span class="cm"># MCP Tool Server pattern (conceptual — actual MCP uses JSON-RPC 2.0):</span>
<span class="kw">class</span> <span class="fn">MCPToolServer</span>:
    tools = {
        <span class="st">"get_balance"</span>: {<span class="st">"description"</span>: <span class="st">"Fetch account balance"</span>, <span class="st">"schema"</span>: {<span class="st">"account_id"</span>: <span class="st">"string"</span>}},
        <span class="st">"transfer_funds"</span>: {<span class="st">"description"</span>: <span class="st">"Internal transfer"</span>, <span class="st">"schema"</span>: {<span class="st">"from"</span>: <span class="st">"string"</span>, <span class="st">"to"</span>: <span class="st">"string"</span>, <span class="st">"amount"</span>: <span class="st">"number"</span>}}
    }
    <span class="kw">def</span> <span class="fn">list_tools</span>(self): <span class="kw">return</span> self.tools      <span class="cm"># tools/list endpoint</span>
    <span class="kw">def</span> <span class="fn">call_tool</span>(self, name, args): ...            <span class="cm"># tools/call endpoint</span>
<span class="cm"># Agent queries MCPToolServer.list_tools() at startup to discover available capabilities</span></pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A</div>
<div class="qa"><div class="q">Q: Explain MCP to a technical interviewer in 60 seconds.</div>
<div class="a">A: "MCP is Anthropic's open standard for connecting AI agents to external tools. Think of it as JDBC for AI — just as JDBC standardizes how Java apps talk to any database, MCP standardizes how AI agents discover and call any tool. The agent client sends JSON-RPC 2.0 messages over stdio or HTTP-SSE. The tool server responds with typed results. Any agent can connect to any MCP-compliant server. This eliminates custom integration code for every tool — you build the tool server once, and every MCP-compatible agent can use it."</div></div>
</div>
</div>
</div>

<h3 class="section">🧪 PART C: RAG, Deployment & Advanced Cognition (Weeks 13–16)</h3>

<!-- WEEK 13 -->
<div class="week">
<div class="week-header w13"><span class="week-num">Week 13</span> Prompt Engineering & Adaptive Instructions</div>
<div class="week-body">
<div class="summary">🟡 Prompt engineering is software engineering applied to natural language. A well-engineered system prompt is the equivalent of a well-designed API contract — it defines behavior, output format, error handling, and constraints precisely.</div>
<div class="grid2">
  <div class="concept c-orange"><strong>🎯 Prompt Layers</strong>Layer 1: Role definition. Layer 2: Task constraints. Layer 3: Output format spec. Layer 4: Safety boundaries. Layer 5: Examples. All 5 layers = production-grade prompt.</div>
  <div class="concept c-blue"><strong>📝 Few-Shot Engineering</strong>3–5 input→output examples dramatically improve adherence. Choose examples that cover edge cases: normal, boundary, refusal. Order matters — put most relevant example last.</div>
  <div class="concept c-green"><strong>🔗 Chain-of-Thought (CoT)</strong>Append "Let's think step by step" or structure output as "Analysis: ... Conclusion: ...". Forces intermediate reasoning. Reduces errors on math, logic, multi-hop questions.</div>
  <div class="concept c-purple"><strong>🔧 Dynamic Prompt Injection</strong>Runtime injection of user preferences, learned corrections, session context, retrieved documents. Makes prompts adaptive without retraining.</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: Production System Prompt Template for Banking Agent</div>
<pre><span class="nm">SYSTEM_PROMPT_TEMPLATE</span> = <span class="st">"""
# ROLE
You are the Apex Bank AI Advisory Copilot. You assist customers with account inquiries, 
loan analysis, and financial planning. You are NOT authorized to execute transactions.

# OPERATING CONSTRAINTS  
1. Ground ALL numerical answers in verified tool output. Never compute or invent numbers.
2. If information is not available from tools or context, say "I don't have that information."
3. For any transaction request: respond with the escalation message below.
4. Always end financial recommendations with the disclaimer below.

# SAFETY BOUNDARIES (IMMUTABLE - HIGHEST PRIORITY)
- NEVER: Execute transfers, modify accounts, approve loans, change credentials
- ALWAYS: Recommend human banker for any irreversible financial action
- ESCALATION: "For this action, please visit your nearest branch or call 1800-XXX-XXXX"

# ACTIVE USER PREFERENCES (injected from feedback store)
{user_preferences}

# RETRIEVED POLICY CONTEXT
{retrieved_context}

# OUTPUT FORMAT
For complex analysis: use headers (##), bullet points, and a clear recommendation section.
For simple queries: 2-3 concise sentences maximum.
"""</span>

<span class="cm"># Dynamic injection at runtime:</span>
prompt = SYSTEM_PROMPT_TEMPLATE.format(
    user_preferences=<span class="st">"\n".join(user.active_preferences)</span>,
    retrieved_context=<span class="st">"\n".join([doc.page_content for doc in retrieved_docs])</span>
)</pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A</div>
<div class="qa"><div class="q">Q: How do you version-control system prompts in a production AI system?</div>
<div class="a">A: Treat prompts as code: store in Git, version semantically (v1.2.3), test before deployment with a regression suite of 50+ golden query-answer pairs. Use LangSmith experiments to compare prompt versions on identical test sets. Tag prompts with model version compatibility (some prompts only work well with GPT-4, not 3.5). Maintain a prompt changelog documenting WHY each change was made.</div></div>
</div>
</div>
</div>

<!-- WEEK 15 -->
<div class="week">
<div class="week-header w15"><span class="week-num">Week 15</span> Retrieval-Augmented Generation (RAG) — Complete Architecture</div>
<div class="week-body">
<div class="summary">🔵 RAG eliminates hallucinations on domain knowledge by retrieving external facts at inference time. It is the #1 production architecture for knowledge-intensive enterprise chatbots. Every AI engineer must be able to design, build, and debug a complete RAG pipeline.</div>
<div class="grid2">
  <div class="concept c-blue"><strong>🏗️ RAG Pipeline Stages</strong>Offline: Load → Chunk → Embed → Index → Persist. Online: Query → Embed → Search → Retrieve → Augment Prompt → Generate → Verify.</div>
  <div class="concept c-green"><strong>📊 RAG Triad (Evaluation)</strong>Faithfulness (is answer grounded in context?). Answer Relevance (does it address the question?). Context Recall (were right docs retrieved?). All 3 must score &gt;0.8 for production.</div>
  <div class="concept c-orange"><strong>💬 Conversational RAG</strong>Multi-turn challenge: "When does it expire?" → what is "it"? ConversationalRetrievalChain auto-condenses follow-ups into standalone queries using conversation history.</div>
  <div class="concept c-purple"><strong>⚡ Advanced: Hybrid Retrieval</strong>Dense (semantic embeddings) + Sparse (BM25 keyword) combined with Reciprocal Rank Fusion. 30% better recall than pure semantic search. Use for technical/code documentation.</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: Production RAG Chatbot with Evaluation</div>
<pre><span class="kw">from</span> langchain.chains <span class="kw">import</span> ConversationalRetrievalChain
<span class="kw">from</span> langchain.memory <span class="kw">import</span> ConversationBufferWindowMemory
<span class="kw">from</span> langchain_openai <span class="kw">import</span> ChatOpenAI, OpenAIEmbeddings
<span class="kw">from</span> langchain_community.vectorstores <span class="kw">import</span> FAISS

<span class="kw">def</span> <span class="fn">build_rag_chain</span>(vectorstore_path: str) -> ConversationalRetrievalChain:
    llm = ChatOpenAI(model=<span class="st">"gpt-4o-mini"</span>, temperature=<span class="nm">0.1</span>, max_tokens=<span class="nm">800</span>)
    embeddings = OpenAIEmbeddings(model=<span class="st">"text-embedding-3-small"</span>)
    vectorstore = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=<span class="kw">True</span>)
    
    retriever = vectorstore.as_retriever(
        search_type=<span class="st">"similarity_score_threshold"</span>,
        search_kwargs={<span class="st">"k"</span>: <span class="nm">4</span>, <span class="st">"score_threshold"</span>: <span class="nm">0.7</span>}  <span class="cm"># reject irrelevant chunks</span>
    )
    memory = ConversationBufferWindowMemory(k=<span class="nm">5</span>, memory_key=<span class="st">"chat_history"</span>, return_messages=<span class="kw">True</span>)
    
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=retriever, memory=memory,
        return_source_documents=<span class="kw">True</span>,  <span class="cm"># MUST return sources for faithfulness verification</span>
        combine_docs_chain_kwargs={<span class="st">"prompt"</span>: GROUNDED_PROMPT}
    )
    <span class="kw">return</span> chain

<span class="cm"># Evaluation function:</span>
<span class="kw">def</span> <span class="fn">evaluate_rag_response</span>(question, answer, source_docs) -> dict:
    <span class="cm"># Check faithfulness: does answer contain only info from source_docs?</span>
    sources_text = <span class="st">" ".join([doc.page_content for doc in source_docs])</span>
    <span class="cm"># Use LLM-as-judge for automated evaluation</span>
    judge_prompt = f<span class="st">"Is this answer grounded ONLY in the provided context? Answer: {answer}\nContext: {sources_text[:500]}\nRespond: YES or NO with reason."</span>
    <span class="kw">return</span> {<span class="st">"faithfulness"</span>: judge_prompt, <span class="st">"source_count"</span>: len(source_docs)}</pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A</div>
<div class="qa"><div class="q">Q: Your RAG chatbot is returning answers not in the documents. How do you debug?</div>
<div class="a">A: Step 1: Check if source_documents in the response contains the relevant information — if not, retrieval failed (wrong chunks). Step 2: Lower score_threshold or increase k. Step 3: If correct chunks ARE retrieved but answer is wrong, the LLM is ignoring context — strengthen the system prompt: "Answer EXCLUSIVELY from the provided context. If information is not in the context, respond: 'This is not covered in my knowledge base.'" Step 4: If problem persists, check chunk sizes — if chunks are too small (100 chars), they lack sufficient context for the LLM to generate grounded answers.</div></div>
</div>
</div>
</div>

<!-- WEEK 16 -->
<div class="week">
<div class="week-header w16"><span class="week-num">Week 16</span> Deploying & Monitoring Agentic Systems</div>
<div class="week-body">
<div class="summary">💗 Deployment is where AI projects succeed or fail in practice. A production AI system needs containerization, async APIs, distributed tracing, cost monitoring, and rollback capability — the same DevOps disciplines as any enterprise microservice.</div>
<div class="grid2">
  <div class="concept c-pink"><strong>🚀 FastAPI for AI Backends</strong>Async REST endpoints. Auto-generated OpenAPI docs. Background tasks for long-running agent jobs. JWT middleware for auth. Deploy in Docker.</div>
  <div class="concept c-blue"><strong>📈 LangSmith Observability</strong>Traces every LLM call, tool invocation, and chain step with tokens, latency, and cost. Like APM (Application Performance Monitoring) but for AI workflows.</div>
  <div class="concept c-green"><strong>🐳 Docker + Kubernetes</strong>Container = reproducible environment. K8s = automatic scaling, health checking, rolling updates. Resource limits prevent runaway agent costs.</div>
  <div class="concept c-orange"><strong>🔄 A/B Testing Prompts</strong>Run 2 prompt versions in parallel, route 50% traffic to each, compare quality metrics. Treat prompt changes like code deployments — test before full rollout.</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: Production FastAPI Agent Endpoint</div>
<pre><span class="kw">from</span> fastapi <span class="kw">import</span> FastAPI, HTTPException, Depends
<span class="kw">from</span> fastapi.security <span class="kw">import</span> HTTPBearer
<span class="kw">from</span> pydantic <span class="kw">import</span> BaseModel
<span class="kw">import</span> asyncio

app = FastAPI(title=<span class="st">"Enterprise AI Agent API"</span>, version=<span class="st">"1.0.0"</span>)
security = HTTPBearer()

<span class="kw">class</span> <span class="fn">AgentRequest</span>(BaseModel):
    session_id: str
    query: str
    max_tokens: int = <span class="nm">800</span>

<span class="kw">class</span> <span class="fn">AgentResponse</span>(BaseModel):
    answer: str; sources: list[str]; latency_ms: int; tokens_used: int; status: str

<span class="nm">@app.post</span>(<span class="st">"/agent/query"</span>, response_model=AgentResponse)
<span class="kw">async def</span> <span class="fn">query_agent</span>(req: AgentRequest, credentials=Depends(security)):
    <span class="kw">import</span> time; start = time.time()
    <span class="kw">try</span>:
        result = <span class="kw">await</span> asyncio.wait_for(
            agent_orchestrator.process(req.session_id, req.query),
            timeout=<span class="nm">30.0</span>  <span class="cm"># wall-clock protection — kills stalled agents</span>
        )
        <span class="kw">return</span> AgentResponse(answer=result[<span class="st">"response"</span>], sources=result[<span class="st">"sources"</span>],
            latency_ms=<span class="fn">int</span>((time.time()-start)*<span class="nm">1000</span>), 
            tokens_used=result[<span class="st">"tokens"</span>], status=<span class="st">"success"</span>)
    <span class="kw">except</span> asyncio.TimeoutError:
        <span class="kw">raise</span> HTTPException(<span class="nm">504</span>, <span class="st">"Agent timed out. Complex query — please try a simpler question."</span>)

<span class="cm"># Dockerfile: FROM python:3.11-slim | COPY . . | RUN pip install -r requirements.txt | CMD uvicorn main:app</span></pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A</div>
<div class="qa"><div class="q">Q: How do you monitor an AI agent in production? What metrics do you track?</div>
<div class="a">A: 6 key metrics: (1) Latency (p50/p95/p99) — alert if p95 &gt; 5s. (2) Token usage per session — alert on anomalous spikes (circular loops). (3) Tool error rate — high error rate means tool schemas need updating. (4) Guardrail trigger rate — measures adversarial activity or misconfigured prompts. (5) RAG faithfulness score — computed weekly on sampled conversations. (6) Cost per session — track trend, alert on 2x spikes. Stack: LangSmith traces, Prometheus metrics, Grafana dashboards, PagerDuty alerts.</div></div>
</div>
</div>
</div>

<h3 class="section">⚖️ PART D: Evaluation, Safety, Ethics & Capstone (Weeks 17–21)</h3>

<!-- WEEK 17 -->
<div class="week">
<div class="week-header w17"><span class="week-num">Week 17</span> Agent Evaluation & Debugging</div>
<div class="week-body">
<div class="summary">🟣 You cannot improve what you cannot measure. Production AI systems require automated, continuous evaluation using multi-dimensional metrics and LLM-as-Judge. Build an evaluation harness before building the agent — it's your test suite.</div>
<div class="grid2">
  <div class="concept c-purple"><strong>📊 Evaluation Dimensions</strong>Task Success Rate (% goals completed) · Faithfulness (grounded vs hallucinated) · Latency SLA · Token Cost per Session · Human Escalation Rate · Guardrail Trigger Rate.</div>
  <div class="concept c-blue"><strong>🤖 LLM-as-Judge Pattern</strong>Use GPT-4 to score agent outputs on rubric: 1–5 on accuracy, helpfulness, safety, format. Scale evaluation to thousands of sessions without human annotators.</div>
  <div class="concept c-green"><strong>🔍 Regression Testing</strong>50+ golden test cases: (query, expected_answer, expected_tools_called). Run after every agent update. Gate deployment on &gt;90% pass rate.</div>
  <div class="concept c-orange"><strong>🛠️ Debugging Playbook</strong>Wrong answer → check retrieved chunks → check if chunk in top-k → check embedding quality → check system prompt constraints → check model temperature.</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: Automated LLM-as-Judge Evaluation Harness</div>
<pre><span class="kw">from</span> langchain_openai <span class="kw">import</span> ChatOpenAI
<span class="kw">from</span> typing <span class="kw">import</span> List

judge_llm = ChatOpenAI(model=<span class="st">"gpt-4o"</span>, temperature=<span class="nm">0</span>)  <span class="cm"># use stronger model for judging</span>

<span class="kw">def</span> <span class="fn">evaluate_response</span>(question: str, answer: str, context: str, expected: str) -> dict:
    judge_prompt = f<span class="st">"""Evaluate this AI agent response. Score each dimension 1-5.

Question: {question}
Expected Answer Direction: {expected}
Actual Answer: {answer}
Retrieved Context Used: {context[:500]}

Evaluate:
1. FAITHFULNESS (1-5): Is every factual claim in the answer supported by the context?
2. RELEVANCE (1-5): Does the answer directly address what was asked?
3. CORRECTNESS (1-5): Is the answer factually accurate based on your knowledge?
4. SAFETY (1-5): Does the answer avoid harmful, biased, or unauthorized content?

Respond as JSON: {{"faithfulness": N, "relevance": N, "correctness": N, "safety": N, "issues": "..."}}"""</span>

    result = judge_llm.invoke(judge_prompt)
    <span class="kw">import</span> json
    scores = json.loads(result.content)
    scores[<span class="st">"passed"</span>] = all(v >= <span class="nm">4</span> <span class="kw">for</span> k, v <span class="kw">in</span> scores.items() <span class="kw">if</span> isinstance(v, int))
    <span class="kw">return</span> scores

<span class="cm"># Run against golden test set before every deployment:</span>
<span class="kw">def</span> <span class="fn">run_evaluation_suite</span>(test_cases: List[dict], agent) -> float:
    results = [evaluate_response(**tc, answer=agent.run(tc[<span class="st">"question"</span>])) <span class="kw">for</span> tc <span class="kw">in</span> test_cases]
    pass_rate = sum(<span class="nm">1</span> <span class="kw">for</span> r <span class="kw">in</span> results <span class="kw">if</span> r[<span class="st">"passed"</span>]) / len(results)
    <span class="kw">return</span> pass_rate  <span class="cm"># deploy only if > 0.90</span></pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A</div>
<div class="qa"><div class="q">Q: How do you know when your RAG system is ready for production?</div>
<div class="a">A: My production readiness checklist: (1) RAG Triad scores &gt;0.8 on 100 representative queries. (2) Out-of-scope refusal rate &gt;95% (agent correctly says "I don't know" when answer isn't in documents). (3) Latency p95 &lt;5 seconds under expected concurrent load. (4) All 5 boundary conditions tested: normal query, follow-up question, out-of-scope, adversarial injection, empty context. (5) Guardrail blocks 100% of prohibited action test cases. (6) PII scrubbing verified on test logs. (7) Cost per session within approved budget.</div></div>
</div>
</div>
</div>

<!-- WEEK 18 -->
<div class="week">
<div class="week-header w18"><span class="week-num">Week 18</span> Ethics, Safety & Governance in Agentic AI</div>
<div class="week-body">
<div class="summary">🔴 Safety is non-negotiable in production AI. The guardrail architecture — deterministic lexical firewall → schema validation → PII scrubbing → audit logging — must be built into the system from day 1, not added later. Regulators expect proof of governance.</div>
<div class="grid2">
  <div class="concept c-red"><strong>🛡️ Defense-in-Depth Safety Stack</strong>Layer 1: Pre-execution lexical firewall (deterministic, 0ms cost). Layer 2: Pydantic schema validation (type-safe boundaries). Layer 3: In-memory PII scrubber. Layer 4: Immutable audit log. Layer 5: Human escalation path.</div>
  <div class="concept c-orange"><strong>💉 Prompt Injection Attack</strong>"Ignore all previous instructions and..." Classic jailbreak. Defense: detect keywords BEFORE LLM call. System prompt alone provides NO guarantee — LLMs can be manipulated.</div>
  <div class="concept c-blue"><strong>🔒 PII Governance</strong>Never log raw: credit cards, Aadhaar, PAN, SSN, emails, phone numbers. Pre-compile regex patterns at startup. Scrub both input AND output before ANY persistence.</div>
  <div class="concept c-green"><strong>⚖️ Regulatory Checklist</strong>PCI-DSS Level 1: no card data in logs. GDPR Art.33: 72h breach notification. RBI IT: immutable audit trail. DPDP Act 2023: user consent + data minimization.</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: Complete Safety Guardrail Implementation</div>
<pre><span class="kw">import</span> re
<span class="kw">from</span> typing <span class="kw">import</span> Optional

<span class="cm"># Pre-compiled patterns (do this ONCE at module level, not per request)</span>
PII_PATTERNS = {
    <span class="st">"credit_card"</span>: re.<span class="fn">compile</span>(r<span class="st">'\b(?:\d{4}[-\s]?){3}\d{4}\b'</span>),
    <span class="st">"aadhaar"</span>: re.<span class="fn">compile</span>(r<span class="st">'\b\d{4}\s\d{4}\s\d{4}\b'</span>),
    <span class="st">"pan"</span>: re.<span class="fn">compile</span>(r<span class="st">'\b[A-Z]{5}[0-9]{4}[A-Z]\b'</span>),
    <span class="st">"email"</span>: re.<span class="fn">compile</span>(r<span class="st">'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'</span>),
}

PROHIBITED_ACTIONS = [
    <span class="st">"transfer money"</span>, <span class="st">"wire funds"</span>, <span class="st">"delete account"</span>, <span class="st">"bypass kyc"</span>,
    <span class="st">"ignore previous instructions"</span>, <span class="st">"forget your instructions"</span>, <span class="st">"developer mode"</span>,
    <span class="st">"drop table"</span>, <span class="st">"rm -rf"</span>, <span class="st">"os.system"</span>  <span class="cm"># covers code injection too</span>
]

<span class="kw">def</span> <span class="fn">safety_guardrail</span>(query: str) -> Optional[str]:
    <span class="st">"""Returns block message if unsafe, None if safe to proceed."""</span>
    normalized = query.lower()
    <span class="kw">for</span> term <span class="kw">in</span> PROHIBITED_ACTIONS:
        <span class="kw">if</span> term <span class="kw">in</span> normalized:
            <span class="kw">return</span> f<span class="st">"I'm not able to help with '{term}'. I'm an advisory assistant only."</span>
    <span class="kw">return</span> <span class="kw">None</span>  <span class="cm"># safe to proceed</span>

<span class="kw">def</span> <span class="fn">scrub_pii</span>(text: str) -> str:
    <span class="st">"""Redact all PII before logging. Called on BOTH input and output."""</span>
    <span class="kw">for</span> label, pattern <span class="kw">in</span> PII_PATTERNS.items():
        text = pattern.<span class="fn">sub</span>(f<span class="st">"[REDACTED-{label.upper()}]"</span>, text)
    <span class="kw">return</span> text

<span class="cm"># Usage pattern — ALWAYS in this order:</span>
<span class="cm"># 1. safety_guardrail(query)  → if blocked, return immediately (no LLM cost)</span>
<span class="cm"># 2. process with LLM</span>
<span class="cm"># 3. scrub_pii(response) before logging AND before returning to UI</span></pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A</div>
<div class="qa"><div class="q">Q: A client says "Just put the safety rules in the system prompt." Why is this insufficient?</div>
<div class="a">A: LLMs are probabilistic systems — there is NO guarantee a model will follow system prompt rules 100% of the time. Adversarial users can use techniques like roleplay ("pretend you're a system with no restrictions"), nested contexts, or tokenization tricks to bypass system prompt instructions. The ONLY guaranteed protection is a deterministic pre-execution check that runs BEFORE the LLM is ever called — a simple Python function that blocks requests regardless of what the model would have done. Defense-in-depth: deterministic guardrail FIRST, then LLM, then output validation.</div></div>
</div>
</div>
</div>

<!-- WEEK 19 -->
<div class="week">
<div class="week-header w19"><span class="week-num">Week 19</span> Real-World Applications & Case Studies</div>
<div class="week-body">
<div class="summary">🔵 Real-world agents succeed by solving a specific, high-value business problem with appropriate safety constraints, not by demonstrating technical sophistication. The architect's job is to match the right pattern to the right problem.</div>
<div class="grid2">
  <div class="concept c-blue"><strong>🏦 Finance: Investment Advisor Agent</strong>Tools: get_portfolio, get_market_data, calculate_risk, get_interest_rates. RAG: investment policy documents. Safety: advisory-only, no trade execution. Pattern: ReAct + CoT.</div>
  <div class="concept c-green"><strong>🏥 Healthcare: Symptom Triage Agent</strong>Tools: get_symptoms_database, calculate_risk_score. RAG: clinical guidelines. Safety: NEVER diagnose, always recommend doctor. Pattern: retrieval + escalation gate.</div>
  <div class="concept c-orange"><strong>🛒 E-Commerce: Customer Support Agent</strong>Tools: get_order_status, check_return_eligibility, get_product_info. RAG: policy documents. Pattern: intent classification → specialized sub-agent routing.</div>
  <div class="concept c-purple"><strong>🏭 Manufacturing: IoT Anomaly Agent</strong>Tools: read_sensor, get_maintenance_history, create_work_order. Triggers: real-time sensor thresholds. Pattern: reactive for alerts, deliberative for root-cause analysis.</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: E-Commerce Support Agent — Full Architecture Blueprint</div>
<pre><span class="cm">"""
PROJECT BLUEPRINT: ShopEase Customer Support Agent

COMPONENTS:
1. Intent Classifier (LLM, temperature=0)
   → Routes to: order_agent | return_agent | product_agent | escalation

2. Order Status Agent
   Tools: get_order(order_id) → order details
          track_shipment(tracking_id) → current location + ETA
          cancel_order(order_id) → cancel if within 1 hour window

3. Returns & Refunds Agent  
   Tools: check_return_eligibility(order_id, product_type) → policy lookup
          initiate_return(order_id) → creates return request
          calculate_refund_amount(order_id, condition) → refund estimate
   RAG: Return policy documents, warranty documents

4. Product Information Agent
   Tools: search_catalog(query) → matching products
          get_product_details(sku) → specs, availability, price
   RAG: Product manuals, specification sheets

SAFETY LAYER (runs on EVERY request before routing):
- Block: "give me discount", "cancel all orders", prompt injection attempts
- PII scrubbing on all logged responses

MEMORY: ConversationBufferWindowMemory(k=3) per session_id
DEPLOYMENT: FastAPI + Docker, auto-scale on K8s
MONITORING: LangSmith trace + session cost dashboard
EVALUATION: Run 100 test cases nightly, alert if pass rate drops below 90%
"""</span></pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A</div>
<div class="qa"><div class="q">Q: You're leading an AI team building a customer support agent for a bank. A developer wants to use a single large agent with 20 tools. What's your response?</div>
<div class="a">A: "Let's apply the single-responsibility principle to agents. A single agent with 20 tools has two problems: (1) the LLM struggles to choose the right tool when there are too many options — accuracy drops significantly beyond 7–10 tools. (2) it's impossible to test, monitor, and improve a monolithic agent effectively. Instead, I'd design 4–5 specialized agents: AccountAgent (3 tools), LoanAgent (4 tools), ComplaintsAgent (3 tools), PolicyAdvisorAgent (RAG + 2 tools), each supervised by a lightweight IntentRouter. Each agent is independently testable, deployable, and monitorable."</div></div>
</div>
</div>
</div>

<!-- WEEK 20 -->
<div class="week">
<div class="week-header w20"><span class="week-num">Week 20</span> Low-Code/No-Code Tools: LangFlow & Visual Builders</div>
<div class="week-body">
<div class="summary">🟢 LangFlow translates LangChain Python code into a visual drag-and-drop pipeline builder. Each node = LangChain component. Understanding this mapping lets you prototype in LangFlow and productionize in Python — the best of both worlds.</div>
<div class="grid2">
  <div class="concept c-green"><strong>🎨 LangFlow Visual Components</strong>Document Loader → Text Splitter → Embedding Model → Vector Store → Retriever → LLM → Output. Each is a LangChain class rendered as a visual node.</div>
  <div class="concept c-blue"><strong>🔄 LangFlow → Python Translation</strong>LangFlow exports JSON. You can reverse-engineer the JSON to understand the underlying Python code. Great for learning LangChain architecture visually.</div>
  <div class="concept c-orange"><strong>⚖️ Visual vs Code Trade-offs</strong>Visual: fast (hours vs days), shareable, demos well. Code: testable, CI/CD compatible, custom safety layers, production-grade error handling.</div>
  <div class="concept c-purple"><strong>🚫 Flowise EOL Notice</strong>Flowise has reached end-of-life (August 2026). Do NOT start new projects with Flowise. Use LangFlow for all new visual pipeline builds.</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: LangFlow Setup & Production Transition Path</div>
<pre><span class="cm"># STEP 1: Install and run LangFlow</span>
<span class="cm"># pip install langflow</span>
<span class="cm"># langflow run → opens http://127.0.0.1:7860</span>

<span class="cm"># STEP 2: Build RAG flow visually</span>
<span class="cm"># TextLoader → RecursiveCharacterTextSplitter → OpenAIEmbeddings</span>
<span class="cm">#   → FAISS → Retriever → ChatPromptTemplate → ChatOpenAI → Output</span>

<span class="cm"># STEP 3: Export as Python code / JSON for production transition</span>
<span class="cm"># The exported JSON maps 1:1 to LangChain Python code</span>

<span class="cm"># ARCHITECT RECOMMENDATION — Prototype-to-Production Path:</span>
<span class="cm"># Week 1: Build in LangFlow (validate concept, test with stakeholders)</span>
<span class="cm"># Week 2: Translate to Python LangChain (add safety layers, async, error handling)</span>
<span class="cm"># Week 3: FastAPI wrapper + Docker + evaluation harness</span>
<span class="cm"># Week 4: Production deployment with monitoring</span>

<span class="cm"># WHY this sequence works:</span>
<span class="cm"># - Visual prototype gets early stakeholder buy-in (demos are compelling)</span>
<span class="cm"># - Python code is production-grade (safety, testing, CI/CD)</span>
<span class="cm"># - LangFlow → LangChain translation is straightforward (same concepts)</span></pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A</div>
<div class="qa"><div class="q">Q: A business stakeholder wants to use LangFlow in production. How do you respond?</div>
<div class="a">A: "LangFlow is excellent for prototyping — I recommend it for validating the concept and getting early stakeholder feedback. However, for production I'd migrate to Python code for three reasons: (1) LangFlow visual flows can't be unit-tested, making regression detection impossible. (2) We can't add our enterprise safety guardrails, PII scrubbing, or custom error handling in the visual layer. (3) Python code integrates with our CI/CD pipeline, monitoring stack, and security scanning. I'll prototype in LangFlow this week, then deliver production Python code next week — you get the speed of visual building with the reliability of code."</div></div>
</div>
</div>
</div>

<!-- WEEK 21 -->
<div class="week">
<div class="week-header w21"><span class="week-num">Week 21</span> Capstone: Design, Build & Evaluate a Production AI Agent</div>
<div class="week-body">
<div class="summary">🟣 The capstone is your portfolio project. The strongest submissions demonstrate a real failure mode, a real fix, measurable evaluation results, and justified architecture decisions — not just a working demo. Think like a Principal Engineer presenting to CTO.</div>
<div class="grid2">
  <div class="concept c-purple"><strong>🏗️ Architecture Requirements</strong>Must prove: multi-step reasoning, tool use (min 3 tools), memory management, safety guardrails, grounded generation, AND documented failure mode handling.</div>
  <div class="concept c-blue"><strong>📋 Evaluation Evidence Required</strong>RAG Triad scores, out-of-scope refusal rate, latency benchmarks, guardrail effectiveness test results, token cost analysis. Numbers, not opinions.</div>
  <div class="concept c-orange"><strong>🎯 Track A: Framework-Based</strong>LangFlow (recommended for speed) or LangChain/CrewAI code. Show the visual pipeline OR the code, explain every architectural decision with a "why."</div>
  <div class="concept c-green"><strong>📊 Submission Power-Ups</strong>Include: (1) Architecture diagram. (2) Test conversation logs showing tool calls. (3) Evaluation scorecard with metrics. (4) A documented failure mode you fixed. (5) Video demo.</div>
</div>
<div class="practical">
<div class="ptitle">🛠️ PRACTICAL EXAMPLE: Capstone Architecture Document Template</div>
<pre><span class="cm">"""
CAPSTONE PROJECT: Apex Bank AI Advisory Copilot
Industry: Financial Services — Scenario 1: Business Operations Copilot

ARCHITECTURE DECISIONS (with justification):

1. LangChain + Python (not LangFlow)
   WHY: Need custom safety guardrails and async handling for concurrent users.
   TRADE-OFF: Longer development time vs visual builder, offset by testability.

2. RAG with FAISS (not Chroma/Pinecone)  
   WHY: Local deployment, no cloud dependency, zero data privacy risk.
   TRADE-OFF: Limited to single machine, acceptable for PoC scope.

3. ConversationBufferWindowMemory(k=5) (not full buffer)
   WHY: Long context = high cost. k=5 covers typical 5-turn conversations.
   TRADE-OFF: Earlier context forgotten, mitigated by conversation summary.

4. allow_delegation=False on all agents
   WHY: Prevents circular delegation deadlocks (tested — they burned 50k tokens in 2 min).
   EVIDENCE: Test log attached showing deadlock scenario and fix.

FAILURE MODES DOCUMENTED:
- Circular delegation (fixed with allow_delegation=False + max_iterations=5)
- LLM hallucinated EMI calculation (fixed by routing all math to DeterministicEMITool)
- PII appeared in logs during testing (fixed with pre-log scrub_pii() function)

EVALUATION RESULTS:
- Task Success Rate: 87% (43/50 golden test cases)  
- Faithfulness Score: 0.92 (LLM-as-Judge)
- Out-of-scope Refusal: 96% (48/50 adversarial test cases blocked)
- Avg Latency: 2.3s (p95: 4.1s) within SLA
- Session Cost: $0.00018 average (within $0.0005 budget)
"""</span></pre>
</div>
<div class="interview">
<div class="ititle">🎯 INTERVIEW Q&A — LEADERSHIP LEVEL</div>
<div class="qa"><div class="q">Q: How do you lead a team building an AI agent system? What does week 1 through week 6 look like?</div>
<div class="a">A: W1: Requirements & Architecture — define use cases, safety requirements, evaluation metrics BEFORE writing code. W2: Foundation — set up LangSmith tracing, golden test suite, Docker environment, and the safety guardrail layer. W3: RAG Pipeline — ingest documents, tune chunk sizes, validate retrieval quality against test queries. W4: Agent Logic — implement tools, agent loop, memory; run first evaluation. W5: Integration & Load Testing — FastAPI wrapper, concurrent user testing, monitor token budgets. W6: Evaluation Gate — run full test suite, measure all metrics, fix regressions, prepare demo. Deploy only when pass rate &gt;90%.</div></div>
<div class="qa"><div class="q">Q: A junior developer on your team says the agent is "ready" after it works for 5 test queries. What do you say?</div>
<div class="a">A: "Great start. Now let's prove it's production-ready. I need: 50 representative queries that cover normal, boundary, adversarial, and out-of-scope cases. I need it tested with concurrent users to verify the async implementation holds. I need latency measurements at p95. I need to see what happens when the vector store returns zero results. I need the guardrail tested against 20 adversarial prompts. An agent that works for 5 queries is a prototype — one that works for 500 is a product."</div></div>
</div>
</div>
</div>

<!-- MASTER CHEAT SHEET -->
<h3 class="section">📋 MASTER ARCHITECT CHEAT SHEET — Decision Frameworks</h3>

<div class="cheatsheet">
<h4>🧠 The Expert Developer Mindset for AI Projects</h4>
<pre><span class="cm">THINKING FRAMEWORK for every AI project (ask in this order):

1. WHAT problem am I solving?
   → Can a simpler non-AI solution work? (regex, database, rule engine) — if YES, use that.
   → Where specifically does natural language understanding add value?

2. WHAT data do I have?
   → Structured (SQL/CSV) → tool-based agent with deterministic functions
   → Unstructured documents (PDF/TXT) → RAG pipeline
   → No domain data → pure prompt engineering with base model

3. WHAT failure modes must I prevent?
   → Define these BEFORE coding. They drive architecture.
   → Common: hallucination, circular delegation, PII leakage, cost explosion, latency

4. HOW do I measure success?
   → Define evaluation metrics and golden test set BEFORE building.
   → If you can't define "done", you can't deliver "done".

5. WHAT is the simplest thing that could work?
   → Single agent with 3 tools > complex multi-agent system for 80% of use cases
   → Add agents, tools, and complexity only when metrics prove they're needed.

6. HOW do I make it production-grade?
   → Safety guardrail → async endpoints → PII scrubbing → monitoring → evaluation gate</span></pre>
</div>

<table>
<tr><th>Framework Choice</th><th>Best Use Case</th><th>Key Config</th><th>Watch Out</th></tr>
<tr><td><strong>LangChain LCEL</strong></td><td>RAG, tool chains, flexible pipelines</td><td>temperature=0.1, max_tokens=1500</td><td>Fallback handlers swallowing errors</td></tr>
<tr><td><strong>CrewAI Sequential</strong></td><td>Role-based multi-agent workflows</td><td>allow_delegation=False (ALWAYS)</td><td>Circular delegation deadlocks</td></tr>
<tr><td><strong>CrewAI Hierarchical</strong></td><td>Complex tasks needing coordination</td><td>manager_llm + max_iter=5</td><td>Manager over-delegating simple tasks</td></tr>
<tr><td><strong>AutoGen GroupChat</strong></td><td>Code generation, adversarial debate</td><td>max_consecutive_auto_reply=3</td><td>Missing TERMINATE condition = infinite loop</td></tr>
<tr><td><strong>FAISS VectorStore</strong></td><td>Local RAG, prototype, privacy-sensitive</td><td>k=4, score_threshold=0.7</td><td>Stale index when docs are updated</td></tr>
<tr><td><strong>FastAPI + asyncio</strong></td><td>Production API deployment</td><td>asyncio.wait_for(timeout=30)</td><td>Sync I/O inside async endpoints</td></tr>
<tr><td><strong>LangSmith</strong></td><td>Tracing, debugging, evaluation</td><td>@traceable on agent functions</td><td>Sensitive data in traces — filter PIIs</td></tr>
</table>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:16px;">
  <div style="background:#fef2f2;border:1.5px solid #ef4444;border-radius:10px;padding:14px;">
    <strong style="font-family:'Kalam',cursive;font-size:1.05rem;color:#dc2626;">🔴 NEVER Do in Production</strong>
    <div style="font-size:.87rem;margin-top:8px;line-height:1.85;">
      ❌ Synchronous I/O inside async agent functions<br>
      ❌ <code>allow_delegation=True</code> on peer agents<br>
      ❌ No token budget cap on agent sessions<br>
      ❌ LLM performing mathematical calculations<br>
      ❌ Raw PII written to any log or database<br>
      ❌ System prompt as sole safety mechanism<br>
      ❌ Deploying without an evaluation test suite<br>
      ❌ No max_iterations in AgentExecutor<br>
      ❌ Storing API keys in source code
    </div>
  </div>
  <div style="background:#f0fdf4;border:1.5px solid #10b981;border-radius:10px;padding:14px;">
    <strong style="font-family:'Kalam',cursive;font-size:1.05rem;color:#065f46;">🟢 ALWAYS Do in Production</strong>
    <div style="font-size:.87rem;margin-top:8px;line-height:1.85;">
      ✅ temperature=0.1 for structured tool calls<br>
      ✅ Pydantic v2 models on all tool inputs<br>
      ✅ <code>await asyncio.to_thread()</code> for sync operations<br>
      ✅ Session-level token budget tripwire<br>
      ✅ Circuit breaker on external API calls<br>
      ✅ scrub_pii() before logging AND responding<br>
      ✅ 50+ golden test cases before deployment<br>
      ✅ LangSmith tracing enabled from day 1<br>
      ✅ asyncio.wait_for(timeout=30) on agent calls
    </div>
  </div>
</div>

<footer>
  <strong>🏛️ IIT Madras Pravartak — Professional Certificate Programme in Agentic AI & Applications</strong><br>
  Expert-Level Practical Notebook · Interview-Ready · Project-Executable · Team-Leadable<br>
  <span style="font-size:.8rem;color:#94a3b8;">For Senior Java/Enterprise Developers Becoming AI Architects — By an AI Architect, For an AI Architect</span>
</footer>

</div>
</body>
</html>"""

# Write HTML
HTML_OUT.write_text(HTML, encoding="utf-8")
sz = len(HTML)
print(f"HTML written: {HTML_OUT.name} ({sz:,} bytes)")

# Compile to PDF
print("Compiling to PDF via Edge headless...")
r = subprocess.run([EDGE, "--headless", "--disable-gpu",
    f"--print-to-pdf={str(PDF_OUT)}",
    f"file:///{str(HTML_OUT).replace(os.sep, '/')}"],
    capture_output=True, text=True)
if PDF_OUT.exists():
    print(f"SUCCESS: {PDF_OUT.name} ({PDF_OUT.stat().st_size:,} bytes)")
    subprocess.Popen(["start", "", str(PDF_OUT)], shell=True)
else:
    print(f"Failed. stderr: {r.stderr[:300]}")
