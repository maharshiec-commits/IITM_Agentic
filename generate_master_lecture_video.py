"""
================================================================================
IIT MADRAS PRAVARTAK — MASTER LECTURE VIDEO GENERATOR
Generates 1080p Documentary-Style Master Lecture MP4 Video for:
"IITM_MASTER_LECTURE_AGENTIC_AI.md"
================================================================================
"""

import os
import sys
import json
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')
import subprocess
import wave
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import win32com.client

WORKSPACE = Path(r"C:\Users\Maharshi\Documents\IITM_Agentic")
TEMP_DIR = WORKSPACE / "lecture_video_temp"
TEMP_DIR.mkdir(exist_ok=True)

FFMPEG_EXE = r"C:\Users\Maharshi\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
FINAL_VIDEO = WORKSPACE / "IITM_Master_Lecture_Agentic_AI.mp4"
PLAYER_HTML = WORKSPACE / "IITM_MASTER_LECTURE_VIDEO_PLAYER.html"

# Slide Content Specifications based on Part 4 of IITM_MASTER_LECTURE_AGENTIC_AI.md
ACTS = [
    {
        "id": 1,
        "title": "Why Multi-Agent Systems Fail in Production",
        "subtitle": "The $27,000 Circular Delegation Crisis & Event Loop Starvation",
        "badge": "ACT 1: THE ENTERPRISE FAILURE MODE",
        "badge_color": (220, 38, 38),  # Red
        "bullets": [
            "🔴 Crisis: 2 peer agents ping-pong an ambiguous query 140+ times in 5 minutes.",
            "💸 Token Budget Explosion: 1.8M tokens consumed ($27.00/session) hitting HTTP 429 limits.",
            "⚠️ Event Loop Starvation: Synchronous I/O inside async functions freezes all user connections.",
            "🛠️ Core Principle: Agentic AI is NOT a chatbot—it is a distributed state machine."
        ],
        "code_snippet": [
            "# VULNERABLE CODE (Circular Loop):",
            "agent_a = Agent(role='Loan Specialist', allow_delegation=True)  # CRITICAL FLAW",
            "agent_b = Agent(role='Legal Auditor', allow_delegation=True)   # DEADLOCK TRAP",
            "# Query: 'Can I refinance?' -> A delegates to B -> B delegates to A -> CRASH"
        ],
        "voiceover": (
            "Imagine delegating a high-stakes banking transaction to an AI agent, "
            "only to watch your server fleet crash in minutes. Not because the model failed to reason, "
            "but because two autonomous sub-agents entered an infinite delegation loop that incinerated "
            "your API budget. In five minutes, 1.8 million tokens were burned and database connections locked. "
            "This is why enterprise agentic AI is fundamentally a systems engineering problem."
        )
    },
    {
        "id": 2,
        "title": "Python Asyncio Runtimes: Defeating Event Loop Starvation",
        "subtitle": "Synchronous Blocking I/O vs. async def with asyncio.to_thread",
        "badge": "ACT 2: CONCURRENCY & RUNTIME ARCHITECTURE",
        "badge_color": (37, 99, 235),  # Blue
        "bullets": [
            "🔷 Single-Threaded Reality: Python's asyncio event loop coordinates cooperative tasks.",
            "⚠️ The Deadly Trap: Calling requests.get() inside async def halts the entire event loop.",
            "🚀 Threadpool Offloading: Use await asyncio.to_thread(func, args) for CPU math/sync APIs.",
            "⚡ High-Concurrency Scale: Handles 150+ concurrent customer agent sessions with zero dropped pings."
        ],
        "code_snippet": [
            "# ENTERPRISE ASYNC EXECUTION BLUEPRINT:",
            "async def dispatch_tool_async(self, pydantic_input: LoanInput):",
            "    # Offload CPU-bound or blocking I/O to background threadpool",
            "    return await asyncio.to_thread(DeterministicTools.calculate_emi, pydantic_input)",
            "    # Result: Event loop stays non-blocking; WebSocket heartbeats survive!"
        ],
        "voiceover": (
            "Under the hood, Python's cooperative event loop is single-threaded. "
            "The second you execute synchronous I/O or a blocking vector search inside an async agent node, "
            "you freeze the entire process. Every concurrent user connection freezes, and Kubernetes health probes fail. "
            "By offloading deterministic computation to worker threads via asyncio dot to-thread and enforcing native "
            "async protocols across LangChain and CrewAI, your agent runtime achieves massive enterprise concurrency."
        )
    },
    {
        "id": 3,
        "title": "The 3-Layer Enterprise Security Architecture",
        "subtitle": "Deterministic Lexical Firewall, Pydantic Schemas & In-Flight PII Redaction",
        "badge": "ACT 3: SAFETY, SCHEMAS & GOVERNANCE",
        "badge_color": (16, 185, 129),  # Emerald Green
        "bullets": [
            "🛡️ Stage 0 Firewall: Lexical & regex filters intercept wire transfers and prompt injection at zero cost.",
            "📐 Stage 1 Schema Gateway: Pydantic v2 validates types, ranges, and maximum underwriting ceilings.",
            "🔒 Stage 2 In-Memory PII Scrubber: Strips credit cards, Aadhaar, PAN, and emails before logging.",
            "⚖️ Regulatory Compliance: Satisfies PCI-DSS Level 1, GDPR Article 33, and RBI financial data mandates."
        ],
        "code_snippet": [
            "# PRE-EXECUTION DETERMINISTIC GUARDRAIL:",
            "if any(term in raw_query.lower() for term in ['transfer money', 'bypass kyc']):",
            "    return 'Security Notice: Transactional mutations prohibited in advisory mode.'",
            "# IN-MEMORY PII REDACTION BEFORE DISK WRITE:",
            "sanitized_log = PII_PATTERNS['credit_card'].sub('[REDACTED_CARD]', user_input)"
        ],
        "voiceover": (
            "True production resilience requires defense-in-depth. "
            "Stage zero intercepts prompt injection and forbidden transactional mutations before the model is ever invoked. "
            "Stage one binds every tool parameter to rigid Pydantic schemas, ensuring exact floating-point arithmetic "
            "rather than hallucinated token math. And stage two strips sensitive credit cards and national IDs "
            "from in-memory buffers before a single byte reaches disk logs. This is how you guarantee compliance."
        )
    },
    {
        "id": 4,
        "title": "CrewAI & AutoGen Governance: Terminating Infinite Loops",
        "subtitle": "allow_delegation=False, Token Caps & Circuit Breakers",
        "badge": "ACT 4: MULTI-AGENT STATE CONTROL",
        "badge_color": (217, 119, 6),  # Orange
        "bullets": [
            "🛑 Anti-Delegation Locks: Set allow_delegation=False in sequential pipelines to eliminate deadlocks.",
            "📊 Session Token Budget Tracker: Hard cap (4,096 tokens) trips execution if loops occur.",
            "🔌 System Circuit Breaker: Trips to OPEN state after 3 consecutive failures for 30s cooldown.",
            "⏱️ Timeout Fences: Enforce strict 15.0-second timeouts per agent node to prevent stalled workers."
        ],
        "code_snippet": [
            "# HARD TOKEN BUDGET TRIPWIRE:",
            "class SessionTokenBudget:",
            "    async def record_consumption(self, tokens: int):",
            "        self.consumed += tokens",
            "        if self.consumed > self.max_budget:",
            "            raise TokenBudgetBreachedException('CRITICAL CIRCUIT TRIP: Limit Exceeded!')"
        ],
        "voiceover": (
            "Here is the critical design flaw in multi-agent orchestration: peer-to-peer delegation without cycle detection. "
            "When Agent A and Agent B can delegate to each other, an ambiguous prompt creates an uncontrollable ping-pong match. "
            "We eliminate this by enforcing linear pipelines with allow-delegation set to False, strict session token budgets, "
            "and circuit breakers that trip the moment anomalous recursion or downstream API failure is detected."
        )
    },
    {
        "id": 5,
        "title": "The Master Cognitive Pipeline: From Transformer to Production",
        "subtitle": "Model Context Protocol (MCP), LangChain LCEL & Autonomous Swarms",
        "badge": "ACT 5: CAPSTONE ARCHITECTURAL SYNTHESIS",
        "badge_color": (139, 92, 246),  # Violet
        "bullets": [
            "🧠 Cognitive Router: LLM acts as reasoning director, while Python functions execute exact business logic.",
            "🔌 Model Context Protocol: Universal JSON-RPC 2.0 client-server interface eliminates custom glue code.",
            "📈 Adaptive Memory Loop: Dynamically injects learned user feedback rules into runtime system prompt.",
            "🎓 Master Principle: Autonomous agents demand disciplined software engineering and bounded state machines."
        ],
        "code_snippet": [
            "# THE 6-STAGE PRODUCTION PIPELINE:",
            "# 1. Safety Guardrail -> 2. Plan Decompose -> 3. Tool Dispatch (MCP)",
            "# 4. Grounded Synthesis -> 5. Sliding-Window Memory -> 6. PII Telemetry",
            "# Architected for IIT Madras Pravartak Professional Certification"
        ],
        "voiceover": (
            "From raw transformer attention to schema-validated MCP gateways, "
            "autonomous agents demand disciplined software engineering. "
            "Treat your language models as cognitive routers, execute your business logic deterministically, "
            "and govern your state machines with uncompromising boundaries. "
            "You now possess the production blueprint to build, deploy, and scale resilient agentic systems in the enterprise."
        )
    }
]

# ──────────────────────────────────────────────────────────────────────────────
# 1. SLIDE RENDERING VIA PILLOW (1920x1080)
# ──────────────────────────────────────────────────────────────────────────────

def render_slide(act: dict, output_path: Path):
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), color=(10, 15, 29))  # Deep navy background
    draw = ImageDraw.Draw(img)

    # Load system fonts
    try:
        font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 52)
        font_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 26)
        font_badge = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 20)
        font_bullet = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 28)
        font_code = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 22)
        font_footer = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 18)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        font_bullet = ImageFont.load_default()
        font_code = ImageFont.load_default()
        font_footer = ImageFont.load_default()

    # Outer decorative glowing border
    draw.rectangle([(20, 20), (width - 20, height - 20)], outline=(30, 41, 59), width=2)
    draw.rectangle([(24, 24), (width - 24, height - 24)], outline=act["badge_color"], width=3)

    # Top Badge
    badge_text = f"  {act['badge']}  "
    bbox = draw.textbbox((70, 50), badge_text, font=font_badge)
    draw.rounded_rectangle([bbox[0]-5, bbox[1]-4, bbox[2]+5, bbox[3]+4], radius=6, fill=act["badge_color"])
    draw.text((70, 50), badge_text, font=font_badge, fill=(255, 255, 255))

    # Header Title & Subtitle
    draw.text((70, 95), act["title"], font=font_title, fill=(248, 250, 252))
    draw.text((70, 165), act["subtitle"], font=font_sub, fill=(148, 163, 184))

    # Decorative separator line
    draw.line([(70, 210), (width - 70, 210)], fill=(51, 65, 85), width=2)

    # Left Column: Key Architectural Concepts & Bullet Points
    left_x = 70
    left_y = 245
    card_width = 860
    card_height = 700

    # Background card for bullet list
    draw.rounded_rectangle([(left_x, left_y), (left_x + card_width, left_y + card_height)], radius=12, fill=(15, 23, 42), outline=(30, 41, 59), width=2)
    draw.text((left_x + 30, left_y + 25), "PRODUCTION ARCHITECTURAL PRINCIPLES", font=font_badge, fill=act["badge_color"])

    b_y = left_y + 80
    for bullet in act["bullets"]:
        # Word wrap bullet text
        words = bullet.split()
        lines = []
        cur_line = []
        for word in words:
            cur_line.append(word)
            test_w = draw.textlength(" ".join(cur_line), font=font_bullet)
            if test_w > card_width - 80:
                cur_line.pop()
                lines.append(" ".join(cur_line))
                cur_line = [word]
        if cur_line:
            lines.append(" ".join(cur_line))

        for idx, line in enumerate(lines):
            draw.text((left_x + 40 if idx == 0 else left_x + 65, b_y), line, font=font_bullet, fill=(241, 245, 249))
            b_y += 38
        b_y += 24

    # Right Column: Production Code Engine & Terminal View
    right_x = 970
    right_y = 245
    code_width = 880
    code_height = 700

    # Background terminal for code
    draw.rounded_rectangle([(right_x, right_y), (right_x + code_width, right_y + code_height)], radius=12, fill=(2, 6, 23), outline=(30, 41, 59), width=2)

    # Terminal title bar
    draw.rounded_rectangle([(right_x, right_y), (right_x + code_width, right_y + 45)], radius=12, fill=(15, 23, 42))
    draw.ellipse([(right_x + 20, right_y + 16), (right_x + 32, right_y + 28)], fill=(239, 68, 68))
    draw.ellipse([(right_x + 40, right_y + 16), (right_x + 52, right_y + 28)], fill=(245, 158, 11))
    draw.ellipse([(right_x + 60, right_y + 16), (right_x + 72, right_y + 28)], fill=(16, 185, 129))
    draw.text((right_x + 95, right_y + 12), "production_engine.py — Enterprise State Machine Blueprint", font=font_sub, fill=(148, 163, 184))

    # Render code lines with syntax coloring
    c_y = right_y + 75
    for c_line in act["code_snippet"]:
        if c_line.strip().startswith("#"):
            fill_color = (100, 116, 139)  # Slate comment
        elif "class" in c_line or "async def" in c_line or "def " in c_line or "return" in c_line:
            fill_color = (244, 114, 182)  # Pink keyword
        elif "Agent(" in c_line or "SessionTokenBudget" in c_line:
            fill_color = (56, 189, 248)  # Cyan class
        elif "True" in c_line or "False" in c_line:
            fill_color = (251, 191, 36)  # Amber bool
        else:
            fill_color = (226, 232, 240)  # Light gray

        draw.text((right_x + 35, c_y), c_line, font=font_code, fill=fill_color)
        c_y += 34

    # Footer banner
    footer_text = "IIT Madras Pravartak · Professional Certificate Programme in Agentic AI · Master Lecture Video Asset"
    draw.text((70, height - 55), footer_text, font=font_footer, fill=(100, 116, 139))
    draw.text((width - 320, height - 55), f"ACT {act['id']} OF 5 | 1080P MASTER", font=font_footer, fill=act["badge_color"])

    img.save(str(output_path), quality=95)
    print(f"Rendered Slide {act['id']}: {output_path.name}")


# ──────────────────────────────────────────────────────────────────────────────
# 2. AUDIO SYNTHESIS VIA WINDOWS SAPI COM (OFFLINE, RELIABLE)
# ──────────────────────────────────────────────────────────────────────────────

def synthesize_audio(text: str, output_wav: Path):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    stream = win32com.client.Dispatch("SAPI.SpFileStream")
    
    # Set speech rate (-10 to 10; 0 is normal, 1 is brisk conversational)
    speaker.Rate = 0
    speaker.Volume = 100

    stream.Open(str(output_wav), 3)  # 3 = SSFMCreateForWrite
    speaker.AudioOutputStream = stream
    speaker.Speak(text)
    stream.Close()
    
    # Calculate audio duration
    with wave.open(str(output_wav), 'r') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)
    
    print(f"Synthesized Audio {output_wav.name} — Duration: {duration:.2f}s")
    return duration


# ──────────────────────────────────────────────────────────────────────────────
# 3. VIDEO SEGMENT ENCODING & CONCATENATION (FFMPEG)
# ──────────────────────────────────────────────────────────────────────────────

def build_video():
    print("\n" + "="*80)
    print("🎬 IIT MADRAS PRAVARTAK — MASTER LECTURE VIDEO BUILDER")
    print("="*80)

    segment_files = []

    for act in ACTS:
        act_id = act["id"]
        slide_img = TEMP_DIR / f"slide_{act_id}.jpg"
        audio_wav = TEMP_DIR / f"audio_{act_id}.wav"
        segment_mp4 = TEMP_DIR / f"segment_{act_id}.mp4"

        # 1. Render slide
        render_slide(act, slide_img)

        # 2. Synthesize voiceover audio
        duration = synthesize_audio(act["voiceover"], audio_wav)
        total_duration = duration + 1.2  # 1.2s padding for smooth visual transition

        # 3. Encode MP4 segment
        cmd = [
            FFMPEG_EXE,
            "-y",
            "-loop", "1",
            "-i", str(slide_img),
            "-i", str(audio_wav),
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-t", str(total_duration),
            str(segment_mp4)
        ]
        
        print(f"Encoding MP4 segment {act_id}...")
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        segment_files.append(segment_mp4)

    # 4. Concatenate all segments into final MP4
    concat_list_file = TEMP_DIR / "concat_list.txt"
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for seg in segment_files:
            # Use forward slashes for ffmpeg concat list
            p_str = str(seg).replace("\\", "/")
            f.write(f"file '{p_str}'\n")

    print("\nConcatenating segments into Final Master Video...")
    cmd_concat = [
        FFMPEG_EXE,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy",
        str(FINAL_VIDEO)
    ]
    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    if FINAL_VIDEO.exists():
        size_mb = FINAL_VIDEO.stat().st_size / (1024 * 1024)
        print(f"\n🎉 SUCCESS: Master Lecture Video Generated at: {FINAL_VIDEO} ({size_mb:.2f} MB)")
    else:
        print("\n❌ Concatenation failed!")
        return

    # 5. Build Dedicated Interactive Video Player HTML
    build_player_html()


# ──────────────────────────────────────────────────────────────────────────────
# 4. INTERACTIVE HTML5 VIDEO PLAYER WITH CHAPTER NAVIGATION & CAPTIONS
# ──────────────────────────────────────────────────────────────────────────────

def build_player_html():
    chapters_js = []
    current_time = 0.0
    for act in ACTS:
        wav_path = TEMP_DIR / f"audio_{act['id']}.wav"
        with wave.open(str(wav_path), 'r') as wf:
            dur = (wf.getnframes() / float(wf.getframerate())) + 1.2
        chapters_js.append({
            "id": act["id"],
            "title": act["title"],
            "subtitle": act["subtitle"],
            "time": round(current_time, 2),
            "voiceover": act["voiceover"]
        })
        current_time += dur

    player_html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IIT Madras Pravartak — Master Lecture Video Player</title>
  <style>
    :root {{
      --bg: #090d16;
      --card: #111827;
      --border: #1f2937;
      --accent: #38bdf8;
      --text: #f9fafb;
      --text-muted: #9ca3af;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow: hidden;
    }}
    header {{
      background: #030712;
      border-bottom: 1px solid var(--border);
      padding: 14px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .brand {{
      font-weight: 700;
      font-size: 1.15rem;
      color: var(--accent);
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .badge {{
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid #0284c7;
      color: var(--accent);
      padding: 4px 10px;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 600;
    }}
    .main-layout {{
      display: flex;
      flex: 1;
      overflow: hidden;
    }}
    .video-stage {{
      flex: 1;
      display: flex;
      flex-direction: column;
      padding: 20px;
      background: #000;
      align-items: center;
      justify-content: center;
    }}
    video {{
      width: 100%;
      max-width: 1100px;
      border-radius: 8px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.8);
      outline: none;
    }}
    .caption-box {{
      width: 100%;
      max-width: 1100px;
      margin-top: 15px;
      padding: 12px 18px;
      background: rgba(17, 24, 39, 0.9);
      border: 1px solid var(--border);
      border-radius: 8px;
      font-size: 0.98rem;
      line-height: 1.5;
      color: #e2e8f0;
      min-height: 60px;
    }}
    .caption-box strong {{
      color: var(--accent);
    }}
    .sidebar {{
      width: 400px;
      background: var(--card);
      border-left: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      overflow-y: auto;
    }}
    .sidebar-header {{
      padding: 18px 20px;
      border-bottom: 1px solid var(--border);
      font-weight: 700;
      font-size: 1rem;
      color: #f3f4f6;
    }}
    .chapter-item {{
      padding: 16px 20px;
      border-bottom: 1px solid var(--border);
      cursor: pointer;
      transition: background 0.2s;
    }}
    .chapter-item:hover {{
      background: #1f2937;
    }}
    .chapter-item.active {{
      background: rgba(56, 189, 248, 0.12);
      border-left: 4px solid var(--accent);
    }}
    .chap-title {{
      font-weight: 600;
      font-size: 0.95rem;
      margin-bottom: 4px;
      color: #f9fafb;
    }}
    .chap-sub {{
      font-size: 0.8rem;
      color: var(--text-muted);
    }}
  </style>
</head>
<body>

  <header>
    <div class="brand">
      <span>🏛️ IIT Madras Pravartak</span>
      <span style="color:#64748b;">|</span>
      <span>Master Lecture: Enterprise Multi-Agent Architectures</span>
    </div>
    <div class="badge">1080P MASTER VIDEO</div>
  </header>

  <div class="main-layout">
    <div class="video-stage">
      <video id="player" controls autoplay>
        <source src="IITM_Master_Lecture_Agentic_AI.mp4" type="video/mp4">
        Your browser does not support HTML5 video.
      </video>
      <div class="caption-box" id="caption">
        <strong>Narration Script:</strong> Loading master lecture voiceover...
      </div>
    </div>

    <div class="sidebar">
      <div class="sidebar-header">📑 Lecture Chapters (5 Acts)</div>
      <div id="chapters-list"></div>
    </div>
  </div>

  <script>
    const chapters = {json.dumps(chapters_js, indent=2)};
    const video = document.getElementById('player');
    const captionEl = document.getElementById('caption');
    const listEl = document.getElementById('chapters-list');

    // Build sidebar
    chapters.forEach((chap, idx) => {{
      const div = document.createElement('div');
      div.className = 'chapter-item' + (idx === 0 ? ' active' : '');
      div.id = 'chap-' + chap.id;
      div.innerHTML = `
        <div class="chap-title">Act ${{chap.id}}: ${{chap.title}}</div>
        <div class="chap-sub">${{chap.subtitle}}</div>
      `;
      div.onclick = () => {{
        video.currentTime = chap.time;
        video.play();
        setActiveChapter(chap.id);
      }};
      listEl.appendChild(div);
    }});

    function setActiveChapter(id) {{
      document.querySelectorAll('.chapter-item').forEach(el => el.classList.remove('active'));
      const active = document.getElementById('chap-' + id);
      if (active) active.classList.add('active');
    }}

    video.ontimeupdate = () => {{
      const t = video.currentTime;
      let activeChap = chapters[0];
      for (let i = chapters.length - 1; i >= 0; i--) {{
        if (t >= chapters[i].time) {{
          activeChap = chapters[i];
          break;
        }}
      }}
      setActiveChapter(activeChap.id);
      captionEl.innerHTML = `<strong>Act ${{activeChap.id}} [${{activeChap.title}}]:</strong> ${{activeChap.voiceover}}`;
    }};
  </script>
</body>
</html>
"""
    PLAYER_HTML.write_text(player_html_content, encoding="utf-8")
    print(f"Generated Interactive Video Player at: {PLAYER_HTML}")

if __name__ == "__main__":
    build_video()
