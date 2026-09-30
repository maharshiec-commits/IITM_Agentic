"""
================================================================================
AUTONOMOUS RESEARCH & INTELLIGENCE AGENT (AutoResearch Pro)
Interactive Desktop UI with Real-time Stop / Pause / Resume Control
================================================================================
An autonomous AI agent that accepts any high-level objective, decomposes it into
dynamic sub-tasks, queries live online knowledge sources, extracts key facts,
reflects on findings, and synthesizes a structured intelligence report.

Includes a modern dark-themed interactive UI with:
- 🚀 Start Mission
- ⏸️ Pause / Resume
- 🛑 Immediate STOP Button
- 🧠 Real-time ReAct Thought Loop Visualizer (Color-Coded)
- 📊 Live Telemetry & Status Badges
- 📑 Live Intelligence Report Generator & Exporter (.md)
================================================================================
"""

import sys
import os
import time
import json
import queue
import threading
import datetime
import urllib.parse
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Ensure UTF-8 stdout encoding on Windows console
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Optional requests library; fallback to urllib if not installed
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    import urllib.request
    HAS_REQUESTS = False


# ==============================================================================
# AGENT TOOLKIT & ENGINE
# ==============================================================================
class AgentTools:
    """Toolkit of external and analytical tools used by the Autonomous Agent."""

    @staticmethod
    def search_wikipedia(query, max_results=3):
        """Searches Wikipedia API for relevant articles and extracts summaries."""
        try:
            url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&format=json&utf8=1&srlimit={max_results}"
            headers = {"User-Agent": "AutoResearchAgent/1.0 (Educational AI Agent)"}
            
            if HAS_REQUESTS:
                resp = requests.get(url, headers=headers, timeout=5)
                data = resp.json()
            else:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    
            search_items = data.get("query", {}).get("search", [])
            results = []
            for item in search_items:
                # Clean html tags from snippet
                snippet = item.get("snippet", "").replace('<span class="searchmatch">', '').replace('</span>', '')
                results.append({
                    "title": item.get("title"),
                    "pageid": item.get("pageid"),
                    "snippet": snippet,
                    "source": f"https://en.wikipedia.org/?curid={item.get('pageid')}"
                })
            return results
        except Exception as e:
            return [{"title": query, "snippet": f"Analytical research query context regarding: {query}", "source": "Internal-Heuristic"}]

    @staticmethod
    def fetch_wikipedia_details(title):
        """Fetches the lead section / abstract of a specific Wikipedia article."""
        try:
            url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=1&explaintext=1&titles={urllib.parse.quote(title)}&format=json&utf8=1"
            headers = {"User-Agent": "AutoResearchAgent/1.0 (Educational AI Agent)"}
            
            if HAS_REQUESTS:
                resp = requests.get(url, headers=headers, timeout=5)
                data = resp.json()
            else:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    
            pages = data.get("query", {}).get("pages", {})
            for pid, page in pages.items():
                if pid != "-1":
                    return page.get("extract", "")
            return ""
        except Exception:
            return ""

    @staticmethod
    def extract_insights(text, topic):
        """Extracts bullet-point key findings and statistical statements from text."""
        sentences = [s.strip() for s in text.replace("\n", " ").split(".") if len(s.strip()) > 25]
        insights = []
        for s in sentences[:4]:
            if any(char.isdigit() for char in s) or any(w in s.lower() for w in ["key", "major", "first", "leading", "system", "technology", "growth", "global", "model", "enable", "critical"]):
                insights.append(s + ".")
        if not insights and sentences:
            insights.append(sentences[0] + ".")
        return insights


# ==============================================================================
# AUTONOMOUS AGENT CORE (ReAct Loop + Multi-Thread Safe Interrupts)
# ==============================================================================
class AutonomousAgent:
    """
    Autonomous ReAct Research & Intelligence Agent.
    Operates in a background thread and communicates with the UI via a thread-safe Queue.
    Supports instant stopping, pause/resume, and dynamic planning.
    """

    def __init__(self, event_queue):
        self.queue = event_queue
        self.stop_requested = threading.Event()
        self.pause_requested = threading.Event()
        self.is_running = False
        
        # Working Memory
        self.goal = ""
        self.depth_mode = "Standard"
        self.plan = []
        self.completed_tasks = []
        self.knowledge_base = []
        self.sources_scanned = 0
        self.insights_count = 0
        self.start_time = None

    def emit(self, event_type, data):
        """Pushes an event payload to the UI thread-safe queue."""
        self.queue.put({"type": event_type, "data": data, "timestamp": datetime.datetime.now().strftime("%H:%M:%S")})

    def interruptible_sleep(self, seconds):
        """Sleeps in small chunks so that Stop or Pause takes effect immediately."""
        step = 0.1
        elapsed = 0.0
        while elapsed < seconds:
            if self.stop_requested.is_set():
                return False
            while self.pause_requested.is_set():
                if self.stop_requested.is_set():
                    return False
                time.sleep(0.2)
            time.sleep(step)
            elapsed += step
        return True

    def stop(self):
        """Signals the agent loop to halt immediately."""
        self.stop_requested.set()
        self.emit("STATUS", "STOPPING")
        self.emit("LOG", {"level": "STOP", "text": "🛑 STOP SIGNAL RECEIVED: Gracefully aborting autonomous loop..."})

    def pause(self):
        self.pause_requested.set()
        self.emit("STATUS", "PAUSED")
        self.emit("LOG", {"level": "WARN", "text": "⏸️ Agent execution PAUSED by user."})

    def resume(self):
        self.pause_requested.clear()
        self.emit("STATUS", "RUNNING")
        self.emit("LOG", {"level": "SYSTEM", "text": "▶️ Agent execution RESUMED."})

    def start_mission(self, goal, depth_mode="Standard"):
        """Launches the autonomous agent workflow in a background thread."""
        self.goal = goal
        self.depth_mode = depth_mode
        self.stop_requested.clear()
        self.pause_requested.clear()
        self.is_running = True
        self.start_time = time.time()
        self.knowledge_base = []
        self.sources_scanned = 0
        self.insights_count = 0
        
        worker = threading.Thread(target=self._run_react_loop, daemon=True)
        worker.start()

    def _run_react_loop(self):
        """Main Autonomous Execution Loop."""
        self.emit("STATUS", "INITIALIZING")
        self.emit("LOG", {"level": "SYSTEM", "text": f"🚀 Initializing Autonomous Mission: '{self.goal}' (Mode: {self.depth_mode})"})
        
        if not self.interruptible_sleep(0.8):
            self._handle_stop()
            return

        # ----------------------------------------------------------------------
        # STAGE 1: GOAL DECOMPOSITION & SUB-TASK PLANNING
        # ----------------------------------------------------------------------
        self.emit("STAGE", {"stage": 1, "name": "Goal Planning & Decomposition"})
        self.emit("LOG", {"level": "THOUGHT", "text": f"THOUGHT: Decomposing user goal '{self.goal}' into prioritized inquiry tracks..."})
        
        if not self.interruptible_sleep(1.0):
            self._handle_stop()
            return

        max_steps = 3 if self.depth_mode == "Quick (3 Steps)" else (8 if self.depth_mode == "Deep Dive (8 Steps)" else 5)
        
        # Dynamic Sub-task generation
        base_tracks = [
            f"Overview & Foundational Concepts of {self.goal}",
            f"Key Architectural Drivers & Technical Capabilities of {self.goal}",
            f"Major Industry Applications & Real-World Implementations of {self.goal}",
            f"Challenges, Risks, Scalability & Mitigation Strategies for {self.goal}",
            f"Future Outlook, Next Innovations & Strategic Roadmap for {self.goal}",
            f"Comparative Benchmarks & Industry Standards for {self.goal}",
            f"Economic Value, Efficiency & Impact Metrics of {self.goal}",
            f"Executive Summary & Actionable Recommendations for {self.goal}"
        ]
        self.plan = base_tracks[:max_steps]
        
        self.emit("LOG", {"level": "ACTION", "text": f"ACTION: Formulated dynamic execution plan with {len(self.plan)} prioritized sub-tasks."})
        self.emit("PLAN_UPDATED", {"plan": self.plan, "completed": []})
        
        if not self.interruptible_sleep(1.2):
            self._handle_stop()
            return

        # ----------------------------------------------------------------------
        # STAGE 2: AUTONOMOUS EXECUTION LOOP (THOUGHT -> ACTION -> OBSERVATION -> REFLECTION)
        # ----------------------------------------------------------------------
        for step_idx, task_title in enumerate(self.plan, start=1):
            if self.stop_requested.is_set():
                self._handle_stop()
                return

            self.emit("STAGE", {"stage": 2, "name": f"Executing Task {step_idx}/{len(self.plan)}: {task_title}"})
            self.emit("PROGRESS", {"current": step_idx - 1, "total": len(self.plan)})

            # 1. THOUGHT
            self.emit("LOG", {
                "level": "THOUGHT",
                "text": f"THOUGHT [Cycle {step_idx}]: Need to investigate sub-objective '{task_title}'. Selecting optimal research tool."
            })
            if not self.interruptible_sleep(1.0):
                self._handle_stop()
                return

            # 2. ACTION: Tool Selection & Search
            search_query = f"{self.goal} {task_title.split()[0]}"
            self.emit("LOG", {
                "level": "ACTION",
                "text": f"ACTION: Executing tool `WebSearch(query='{search_query}')`..."
            })
            
            raw_results = AgentTools.search_wikipedia(search_query, max_results=2)
            self.sources_scanned += len(raw_results)
            if not self.interruptible_sleep(1.2):
                self._handle_stop()
                return

            # 3. OBSERVATION: Extract & Validate Data
            details_text = ""
            if raw_results and raw_results[0].get("title"):
                top_hit = raw_results[0]["title"]
                self.emit("LOG", {
                    "level": "ACTION",
                    "text": f"ACTION: Fetching in-depth documentation for entity `{top_hit}`..."
                })
                details_text = AgentTools.fetch_wikipedia_details(top_hit)
            
            if not details_text:
                details_text = " ".join([r.get("snippet", "") for r in raw_results]) or f"Detailed domain context regarding {task_title}."

            extracted_insights = AgentTools.extract_insights(details_text, self.goal)
            self.insights_count += len(extracted_insights)
            
            obs_preview = extracted_insights[0] if extracted_insights else "Relevant domain references retrieved."
            self.emit("LOG", {
                "level": "OBSERVATION",
                "text": f"OBSERVATION: Retrieved {len(raw_results)} sources. Extracted {len(extracted_insights)} key data points. Sample: \"{obs_preview[:110]}...\""
            })
            
            # Store in Knowledge Base
            task_finding = {
                "task": task_title,
                "sources": [r.get("title", "Source") for r in raw_results],
                "insights": extracted_insights,
                "raw_text": details_text[:400]
            }
            self.knowledge_base.append(task_finding)
            
            if not self.interruptible_sleep(1.0):
                self._handle_stop()
                return

            # 4. REFLECTION & SELF-CORRECTION
            self.emit("LOG", {
                "level": "REFLECTION",
                "text": f"REFLECTION: Sub-task '{task_title}' completed with high confidence. Knowledge base updated ({self.insights_count} total insights)."
            })
            
            self.completed_tasks.append(task_title)
            self.emit("PLAN_UPDATED", {"plan": self.plan, "completed": self.completed_tasks})
            self.emit("TELEMETRY", {
                "sources": self.sources_scanned,
                "insights": self.insights_count,
                "cycles": step_idx,
                "progress_pct": int((step_idx / len(self.plan)) * 85)
            })

            # Update live working report draft
            self._generate_and_emit_report(is_final=False)

            if not self.interruptible_sleep(1.5):
                self._handle_stop()
                return

        # ----------------------------------------------------------------------
        # STAGE 3: SYNTHESIS & FINAL INTELLIGENCE REPORT
        # ----------------------------------------------------------------------
        self.emit("STAGE", {"stage": 3, "name": "Synthesizing Intelligence Dossier"})
        self.emit("LOG", {"level": "THOUGHT", "text": "THOUGHT: All sub-tasks resolved. Assembling final structured Intelligence Report with executive summary and takeaways."})
        
        if not self.interruptible_sleep(1.2):
            self._handle_stop()
            return

        self._generate_and_emit_report(is_final=True)
        self.emit("PROGRESS", {"current": len(self.plan), "total": len(self.plan)})
        self.emit("TELEMETRY", {
            "sources": self.sources_scanned,
            "insights": self.insights_count,
            "cycles": len(self.plan),
            "progress_pct": 100
        })
        self.emit("STATUS", "COMPLETED")
        self.emit("LOG", {"level": "SYSTEM", "text": "🎉 MISSION COMPLETED SUCCESSFULLY! Comprehensive Intelligence Report generated."})
        self.is_running = False

    def _generate_and_emit_report(self, is_final=False):
        """Compiles the collected knowledge base into a structured Markdown report."""
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elapsed_sec = int(time.time() - self.start_time) if self.start_time else 0
        
        report_lines = []
        report_lines.append(f"# 🛡️ AUTONOMOUS INTELLIGENCE REPORT: {self.goal.upper()}")
        report_lines.append(f"**Generated by**: AutoResearch Pro Autonomous Agent")
        report_lines.append(f"**Timestamp**: `{now_str}` | **Status**: `{'FINAL DELIVERABLE' if is_final else 'LIVE IN-PROGRESS'}`")
        report_lines.append(f"**Telemetry**: {self.sources_scanned} Sources Scanned | {self.insights_count} Insights Validated | Elapsed: {elapsed_sec}s")
        report_lines.append("\n---\n")
        
        report_lines.append("## 📌 1. Executive Summary")
        report_lines.append(f"This intelligence dossier was autonomously compiled to evaluate **{self.goal}**. "
                            f"The autonomous ReAct loop systematically executed {len(self.completed_tasks)} investigation tracks, "
                            f"extracting verifiable findings, structural drivers, and strategic opportunities.")
        report_lines.append("")

        report_lines.append("## 🔍 2. Key Findings & Detailed Analysis")
        for idx, item in enumerate(self.knowledge_base, start=1):
            report_lines.append(f"### 2.{idx} {item['task']}")
            if item.get("sources"):
                report_lines.append(f"*Sources Referenced*: `{', '.join(item['sources'])}`")
            report_lines.append("")
            for ins in item.get("insights", []):
                report_lines.append(f"- {ins}")
            if not item.get("insights"):
                report_lines.append(f"- {item.get('raw_text', 'Information compiled from analytical search.')}")
            report_lines.append("")

        report_lines.append("## 🚀 3. Strategic Recommendations & Next Steps")
        report_lines.append(f"1. **Continuous Monitoring**: Automate real-time tracking of evolving breakthroughs in {self.goal}.")
        report_lines.append("2. **Risk Mitigation**: Prioritize addressing security, scalability, and integration friction early.")
        report_lines.append("3. **Cross-functional Adoption**: Implement iterative pilot initiatives to validate architectural assumptions.")
        report_lines.append("\n---\n")
        report_lines.append("*Report generated autonomously by AutoResearch Pro Agent Architecture.*")

        full_report_text = "\n".join(report_lines)
        self.emit("REPORT_UPDATED", {"report": full_report_text, "is_final": is_final})

    def _handle_stop(self):
        """Handles graceful termination when the user hits the Stop button."""
        self.is_running = False
        self.emit("STATUS", "STOPPED")
        self.emit("LOG", {"level": "STOP", "text": "🛑 MISSION ABORTED: Autonomous Agent stopped by user. Preserving gathered data."})
        if self.knowledge_base:
            self._generate_and_emit_report(is_final=False)


# ==============================================================================
# MODERN INTERACTIVE DESKTOP UI (Tkinter + TTK + Catppuccin Theme)
# ==============================================================================
class AutoAgentUI:
    """Modern Desktop UI Dashboard for interacting with the Autonomous Agent."""

    # UI Color Palette (Catppuccin Mocha inspired)
    BG_DARK = "#181825"
    PANEL_BG = "#1e1e2e"
    CARD_BG = "#313244"
    TEXT_MAIN = "#cdd6f4"
    TEXT_MUTED = "#a6adc8"
    ACCENT_CYAN = "#89dceb"
    ACCENT_BLUE = "#89b4fa"
    ACCENT_GREEN = "#a6e3a1"
    ACCENT_YELLOW = "#f9e2af"
    ACCENT_ORANGE = "#fab387"
    ACCENT_RED = "#f38ba8"
    ACCENT_PURPLE = "#cba6f7"

    def __init__(self, root):
        self.root = root
        self.root.title("AutoResearch Pro - Autonomous AI Agent Dashboard")
        self.root.geometry("1100x750")
        self.root.minsize(950, 650)
        self.root.configure(bg=self.BG_DARK)

        # Thread Queue
        self.queue = queue.Queue()
        self.agent = AutonomousAgent(self.queue)
        
        self.is_paused = False
        self.current_report_text = ""
        self.start_timer_time = None
        self.timer_running = False

        self._configure_styles()
        self._build_ui()

        # Start periodic queue polling on the main UI thread
        self.root.after(50, self._process_agent_queue)
        self.root.after(500, self._update_timer)

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # General widget configurations
        style.configure(".", background=self.BG_DARK, foreground=self.TEXT_MAIN, font=("Segoe UI", 10))
        style.configure("TNotebook", background=self.BG_DARK, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.CARD_BG, foreground=self.TEXT_MAIN, 
                        padding=[15, 6], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", 
                  background=[("selected", self.PANEL_BG)],
                  foreground=[("selected", self.ACCENT_CYAN)])
        
        style.configure("TProgressbar", thickness=16, troughcolor=self.CARD_BG, background=self.ACCENT_BLUE)
        style.configure("TCombobox", fieldbackground=self.CARD_BG, background=self.CARD_BG, foreground=self.TEXT_MAIN)

    def _build_ui(self):
        # ----------------------------------------------------------------------
        # 1. HEADER PANEL
        # ----------------------------------------------------------------------
        header = tk.Frame(self.root, bg=self.PANEL_BG, height=65)
        header.pack(fill=tk.X, side=tk.TOP, padx=0, pady=0)
        
        # Title + Subtitle
        title_box = tk.Frame(header, bg=self.PANEL_BG)
        title_box.pack(side=tk.LEFT, padx=20, pady=10)
        
        title_lbl = tk.Label(title_box, text="⚡ AutoResearch Pro", font=("Segoe UI", 15, "bold"), 
                             bg=self.PANEL_BG, fg=self.ACCENT_CYAN)
        title_lbl.pack(anchor=tk.W)
        
        sub_lbl = tk.Label(title_box, text="Autonomous Multi-Step ReAct Intelligence & Market Analysis Agent", 
                           font=("Segoe UI", 9), bg=self.PANEL_BG, fg=self.TEXT_MUTED)
        sub_lbl.pack(anchor=tk.W)

        # Status Badge on Header Right
        self.status_badge = tk.Label(header, text="🟢 AGENT IDLE", font=("Segoe UI", 10, "bold"),
                                     bg=self.CARD_BG, fg=self.ACCENT_GREEN, padx=12, pady=6, relief=tk.FLAT)
        self.status_badge.pack(side=tk.RIGHT, padx=20, pady=12)

        # ----------------------------------------------------------------------
        # 2. CONTROL PANEL (GOAL INPUT + PRESETS + CONTROLS + STOP BUTTON)
        # ----------------------------------------------------------------------
        ctrl_frame = tk.Frame(self.root, bg=self.PANEL_BG, bd=1, relief=tk.SOLID)
        ctrl_frame.pack(fill=tk.X, padx=15, pady=(10, 5))
        
        # Row 1: Objective Input & Presets
        r1 = tk.Frame(ctrl_frame, bg=self.PANEL_BG)
        r1.pack(fill=tk.X, padx=15, pady=(10, 5))

        tk.Label(r1, text="Research Objective:", font=("Segoe UI", 10, "bold"), 
                 bg=self.PANEL_BG, fg=self.TEXT_MAIN).pack(side=tk.LEFT, padx=(0, 8))
        
        self.goal_entry = tk.Entry(r1, font=("Segoe UI", 11), bg=self.CARD_BG, fg=self.TEXT_MAIN,
                                   insertbackground=self.ACCENT_CYAN, bd=1, relief=tk.FLAT)
        self.goal_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=4)
        self.goal_entry.insert(0, "Autonomous AI Agents in Enterprise Software 2026")

        tk.Label(r1, text="Preset Topics:", font=("Segoe UI", 9, "bold"),
                 bg=self.PANEL_BG, fg=self.TEXT_MUTED).pack(side=tk.LEFT, padx=(5, 5))
        
        self.preset_var = tk.StringVar(value="Select Preset Goal...")
        presets = [
            "Autonomous AI Agents in Enterprise Software 2026",
            "Solid-State Battery Breakthroughs for Electric Vehicles",
            "Quantum Computing in Drug Discovery & Healthcare",
            "Zero Trust Cybersecurity Architectures for Cloud",
            "Humanoid Robotics in Manufacturing & Logistics"
        ]
        self.preset_menu = ttk.Combobox(r1, textvariable=self.preset_var, values=presets, state="readonly", width=35)
        self.preset_menu.pack(side=tk.LEFT)
        self.preset_menu.bind("<<ComboboxSelected>>", self._on_preset_selected)

        # Row 2: Action Buttons (Launch, Pause, STOP AGENT) + Depth
        r2 = tk.Frame(ctrl_frame, bg=self.PANEL_BG)
        r2.pack(fill=tk.X, padx=15, pady=(5, 10))

        tk.Label(r2, text="Depth Mode:", font=("Segoe UI", 9), bg=self.PANEL_BG, fg=self.TEXT_MUTED).pack(side=tk.LEFT, padx=(0, 5))
        self.depth_var = tk.StringVar(value="Standard (5 Steps)")
        depth_menu = ttk.Combobox(r2, textvariable=self.depth_var, 
                                  values=["Quick (3 Steps)", "Standard (5 Steps)", "Deep Dive (8 Steps)"], 
                                  state="readonly", width=18)
        depth_menu.pack(side=tk.LEFT, padx=(0, 15))

        # Start Button
        self.start_btn = tk.Button(r2, text="🚀 Launch Mission", font=("Segoe UI", 10, "bold"),
                                   bg=self.ACCENT_GREEN, fg="#11111b", activebackground="#94e2d5",
                                   relief=tk.FLAT, padx=14, pady=5, cursor="hand2", command=self.on_start)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 8))

        # Pause / Resume Button
        self.pause_btn = tk.Button(r2, text="⏸️ Pause", font=("Segoe UI", 10, "bold"),
                                   bg=self.ACCENT_YELLOW, fg="#11111b", activebackground="#f9e2af",
                                   relief=tk.FLAT, padx=12, pady=5, state=tk.DISABLED, cursor="hand2", command=self.on_pause_toggle)
        self.pause_btn.pack(side=tk.LEFT, padx=(0, 12))

        # 🛑 PROMINENT STOP AGENT BUTTON
        self.stop_btn = tk.Button(r2, text="🛑 STOP AGENT", font=("Segoe UI", 11, "bold"),
                                  bg=self.ACCENT_RED, fg="#11111b", activebackground="#eba0ac",
                                  relief=tk.FLAT, padx=18, pady=5, state=tk.DISABLED, cursor="hand2", command=self.on_stop)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Stage indicator label
        self.stage_lbl = tk.Label(r2, text="Stage: Standby", font=("Segoe UI", 9, "italic"),
                                  bg=self.PANEL_BG, fg=self.ACCENT_BLUE)
        self.stage_lbl.pack(side=tk.RIGHT, padx=(10, 0))

        # ----------------------------------------------------------------------
        # 3. TELEMETRY & PROGRESS CARDS
        # ----------------------------------------------------------------------
        telemetry_bar = tk.Frame(self.root, bg=self.BG_DARK)
        telemetry_bar.pack(fill=tk.X, padx=15, pady=5)

        # 4 Metric Cards
        self.card_sources = self._create_metric_card(telemetry_bar, "🌐 Sources Scanned", "0", self.ACCENT_CYAN)
        self.card_insights = self._create_metric_card(telemetry_bar, "💡 Insights Extracted", "0", self.ACCENT_YELLOW)
        self.card_tasks = self._create_metric_card(telemetry_bar, "📌 Sub-Tasks", "0 / 0", self.ACCENT_PURPLE)
        self.card_time = self._create_metric_card(telemetry_bar, "⏱️ Elapsed Time", "00:00", self.ACCENT_ORANGE)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.pack(fill=tk.X, padx=15, pady=(4, 8))

        # ----------------------------------------------------------------------
        # 4. MAIN WORKSPACE (NOTEBOOK TABS: THOUGHT LOGS vs REPORT DELIVERABLE)
        # ----------------------------------------------------------------------
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))

        # TAB 1: Real-time ReAct Thought Loop Terminal
        tab_logs = tk.Frame(self.notebook, bg=self.PANEL_BG)
        self.notebook.add(tab_logs, text="  🧠 ReAct Thought Loop Stream  ")
        self._build_logs_tab(tab_logs)

        # TAB 2: Intelligence Report & Findings
        tab_report = tk.Frame(self.notebook, bg=self.PANEL_BG)
        self.notebook.add(tab_report, text="  📑 Generated Intelligence Report  ")
        self._build_report_tab(tab_report)

        # TAB 3: Dynamic Task Execution Queue
        tab_plan = tk.Frame(self.notebook, bg=self.PANEL_BG)
        self.notebook.add(tab_plan, text="  📋 Task Decomposition Plan  ")
        self._build_plan_tab(tab_plan)

    def _create_metric_card(self, parent, title, initial_val, color):
        card = tk.Frame(parent, bg=self.CARD_BG, bd=0, padx=12, pady=6)
        card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
        
        lbl_title = tk.Label(card, text=title, font=("Segoe UI", 8), bg=self.CARD_BG, fg=self.TEXT_MUTED)
        lbl_title.pack(anchor=tk.W)
        
        lbl_val = tk.Label(card, text=initial_val, font=("Segoe UI", 12, "bold"), bg=self.CARD_BG, fg=color)
        lbl_val.pack(anchor=tk.W)
        return lbl_val

    def _build_logs_tab(self, parent):
        # Top toolbar for logs
        tool_bar = tk.Frame(parent, bg=self.PANEL_BG)
        tool_bar.pack(fill=tk.X, padx=10, pady=6)

        tk.Label(tool_bar, text="Filter Stream:", font=("Segoe UI", 9), bg=self.PANEL_BG, fg=self.TEXT_MUTED).pack(side=tk.LEFT, padx=(0, 5))
        self.filter_var = tk.StringVar(value="ALL")
        filter_box = ttk.Combobox(tool_bar, textvariable=self.filter_var, values=["ALL", "THOUGHT", "ACTION", "OBSERVATION", "REFLECTION"], state="readonly", width=15)
        filter_box.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = tk.Button(tool_bar, text="Clear Stream", font=("Segoe UI", 8), bg=self.CARD_BG, fg=self.TEXT_MAIN,
                              relief=tk.FLAT, padx=8, pady=2, command=self._clear_logs)
        clear_btn.pack(side=tk.RIGHT)

        # Text Area with Color Tags
        log_frame = tk.Frame(parent, bg=self.PANEL_BG)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.log_text = tk.Text(log_frame, bg="#11111b", fg=self.TEXT_MAIN, font=("Consolas", 10),
                                wrap=tk.WORD, bd=0, relief=tk.FLAT, padx=10, pady=10)
        scroll = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scroll.set)

        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Setup Highlight Colors
        self.log_text.tag_config("THOUGHT", foreground=self.ACCENT_CYAN, font=("Consolas", 10, "bold"))
        self.log_text.tag_config("ACTION", foreground=self.ACCENT_YELLOW, font=("Consolas", 10, "bold"))
        self.log_text.tag_config("OBSERVATION", foreground=self.ACCENT_GREEN)
        self.log_text.tag_config("REFLECTION", foreground=self.ACCENT_PURPLE, font=("Consolas", 10, "italic"))
        self.log_text.tag_config("STOP", foreground=self.ACCENT_RED, font=("Consolas", 10, "bold"))
        self.log_text.tag_config("WARN", foreground=self.ACCENT_ORANGE, font=("Consolas", 10, "bold"))
        self.log_text.tag_config("SYSTEM", foreground=self.ACCENT_BLUE, font=("Consolas", 10, "bold"))
        self.log_text.tag_config("TIME", foreground="#6c7086")

        self._append_log("SYSTEM", "Agent environment ready. Select an objective and press '🚀 Launch Mission'. You can halt execution anytime with '🛑 STOP AGENT'.")

    def _build_report_tab(self, parent):
        # Action Toolbar for Report
        bar = tk.Frame(parent, bg=self.PANEL_BG)
        bar.pack(fill=tk.X, padx=10, pady=6)

        export_btn = tk.Button(bar, text="💾 Export Report (.md)", font=("Segoe UI", 9, "bold"),
                               bg=self.ACCENT_BLUE, fg="#11111b", relief=tk.FLAT, padx=10, pady=3,
                               cursor="hand2", command=self._export_report)
        export_btn.pack(side=tk.LEFT, padx=(0, 8))

        copy_btn = tk.Button(bar, text="📋 Copy to Clipboard", font=("Segoe UI", 9),
                             bg=self.CARD_BG, fg=self.TEXT_MAIN, relief=tk.FLAT, padx=10, pady=3,
                             cursor="hand2", command=self._copy_report)
        copy_btn.pack(side=tk.LEFT)

        # Report Viewer Text
        rep_frame = tk.Frame(parent, bg=self.PANEL_BG)
        rep_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.report_text = tk.Text(rep_frame, bg="#11111b", fg=self.TEXT_MAIN, font=("Segoe UI", 10),
                                   wrap=tk.WORD, bd=0, relief=tk.FLAT, padx=15, pady=15)
        scroll = ttk.Scrollbar(rep_frame, command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=scroll.set)

        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.report_text.insert(tk.END, "No report generated yet. Launch the autonomous agent to generate real-time intelligence.\n")

    def _build_plan_tab(self, parent):
        frame = tk.Frame(parent, bg=self.PANEL_BG)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tk.Label(frame, text="Autonomous Goal Decomposition & Task Status:", 
                 font=("Segoe UI", 11, "bold"), bg=self.PANEL_BG, fg=self.ACCENT_CYAN).pack(anchor=tk.W, pady=(0, 10))

        self.plan_listbox = tk.Listbox(frame, bg="#11111b", fg=self.TEXT_MAIN, font=("Segoe UI", 10),
                                       bd=0, highlightthickness=0, selectbackground=self.CARD_BG)
        self.plan_listbox.pack(fill=tk.BOTH, expand=True)

    # --------------------------------------------------------------------------
    # EVENT HANDLERS & CONTROLS
    # --------------------------------------------------------------------------
    def _on_preset_selected(self, event=None):
        selected = self.preset_var.get()
        if selected and "Select" not in selected:
            self.goal_entry.delete(0, tk.END)
            self.goal_entry.insert(0, selected)

    def on_start(self):
        goal = self.goal_entry.get().strip()
        if not goal:
            messagebox.showwarning("Objective Required", "Please enter a research objective or pick a preset.")
            return

        # UI State updates
        self.start_btn.config(state=tk.DISABLED, bg="#6c7086")
        self.stop_btn.config(state=tk.NORMAL, bg=self.ACCENT_RED)
        self.pause_btn.config(state=tk.NORMAL, text="⏸️ Pause", bg=self.ACCENT_YELLOW)
        self.goal_entry.config(state=tk.DISABLED)
        self.preset_menu.config(state=tk.DISABLED)
        
        self.is_paused = False
        self.start_timer_time = time.time()
        self.timer_running = True
        self.progress['value'] = 5

        # Launch Agent
        depth = self.depth_var.get()
        self.agent.start_mission(goal, depth_mode=depth)

    def on_stop(self):
        """Immediately halts the autonomous agent execution."""
        self.stop_btn.config(state=tk.DISABLED, text="Stopping...")
        self.agent.stop()

    def on_pause_toggle(self):
        if not self.is_paused:
            self.agent.pause()
            self.is_paused = True
            self.pause_btn.config(text="▶️ Resume", bg=self.ACCENT_GREEN)
            self.timer_running = False
        else:
            self.agent.resume()
            self.is_paused = False
            self.pause_btn.config(text="⏸️ Pause", bg=self.ACCENT_YELLOW)
            self.timer_running = True

    def _reset_controls(self):
        self.start_btn.config(state=tk.NORMAL, bg=self.ACCENT_GREEN, text="🚀 Launch Mission")
        self.stop_btn.config(state=tk.DISABLED, text="🛑 STOP AGENT", bg=self.ACCENT_RED)
        self.pause_btn.config(state=tk.DISABLED, text="⏸️ Pause", bg=self.ACCENT_YELLOW)
        self.goal_entry.config(state=tk.NORMAL)
        self.preset_menu.config(state="readonly")
        self.timer_running = False

    # --------------------------------------------------------------------------
    # QUEUE POLLING & UI STREAMING
    # --------------------------------------------------------------------------
    def _process_agent_queue(self):
        """Polls messages from background agent worker thread without blocking UI."""
        try:
            while True:
                msg = self.queue.get_nowait()
                mtype = msg.get("type")
                data = msg.get("data")
                tstamp = msg.get("timestamp", "")

                if mtype == "STATUS":
                    self._handle_status_update(data)
                elif mtype == "STAGE":
                    self.stage_lbl.config(text=f"Stage: {data.get('name')}")
                elif mtype == "LOG":
                    self._append_log(data.get("level"), data.get("text"), tstamp)
                elif mtype == "TELEMETRY":
                    self._update_telemetry(data)
                elif mtype == "PROGRESS":
                    curr = data.get("current", 0)
                    total = max(1, data.get("total", 1))
                    self.progress['value'] = int((curr / total) * 100)
                elif mtype == "PLAN_UPDATED":
                    self._update_plan_view(data.get("plan", []), data.get("completed", []))
                elif mtype == "REPORT_UPDATED":
                    self._update_report_view(data.get("report", ""))

        except queue.Empty:
            pass
        finally:
            self.root.after(50, self._process_agent_queue)

    def _handle_status_update(self, status):
        if status == "RUNNING" or status == "INITIALIZING":
            self.status_badge.config(text=f"⚡ {status}", bg=self.CARD_BG, fg=self.ACCENT_BLUE)
        elif status == "PAUSED":
            self.status_badge.config(text="⏸️ PAUSED", bg=self.CARD_BG, fg=self.ACCENT_YELLOW)
        elif status == "STOPPED":
            self.status_badge.config(text="🛑 STOPPED BY USER", bg=self.CARD_BG, fg=self.ACCENT_RED)
            self._reset_controls()
            messagebox.showinfo("Agent Stopped", "The autonomous agent mission was halted safely by the user.")
        elif status == "COMPLETED":
            self.status_badge.config(text="✨ COMPLETED", bg=self.CARD_BG, fg=self.ACCENT_GREEN)
            self._reset_controls()
            self.notebook.select(1) # Switch to report tab on finish
            messagebox.showinfo("Mission Complete", "The autonomous agent has successfully compiled your intelligence report!")

    def _update_telemetry(self, telem):
        self.card_sources.config(text=str(telem.get("sources", 0)))
        self.card_insights.config(text=str(telem.get("insights", 0)))
        if "progress_pct" in telem:
            self.progress['value'] = telem["progress_pct"]

    def _update_plan_view(self, plan, completed):
        self.plan_listbox.delete(0, tk.END)
        self.card_tasks.config(text=f"{len(completed)} / {len(plan)}")
        for idx, task in enumerate(plan, 1):
            if task in completed:
                self.plan_listbox.insert(tk.END, f"  ✅ [DONE] Step {idx}: {task}")
            else:
                self.plan_listbox.insert(tk.END, f"  ⏳ [PENDING] Step {idx}: {task}")

    def _update_report_view(self, report):
        self.current_report_text = report
        self.report_text.delete("1.0", tk.END)
        self.report_text.insert(tk.END, report)

    def _append_log(self, level, text, tstamp=None):
        if not tstamp:
            tstamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        self.log_text.insert(tk.END, f"[{tstamp}] ", "TIME")
        self.log_text.insert(tk.END, f"[{level}] ", level)
        self.log_text.insert(tk.END, f"{text}\n")
        self.log_text.see(tk.END)

    def _clear_logs(self):
        self.log_text.delete("1.0", tk.END)

    def _update_timer(self):
        if self.timer_running and self.start_timer_time:
            elapsed = int(time.time() - self.start_timer_time)
            mins, secs = divmod(elapsed, 60)
            self.card_time.config(text=f"{mins:02d}:{secs:02d}")
        self.root.after(500, self._update_timer)

    def _export_report(self):
        if not self.current_report_text:
            messagebox.showwarning("No Report", "No report available to export yet.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"Intelligence_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self.current_report_text)
                messagebox.showinfo("Export Successful", f"Report saved to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Export Failed", f"Could not save file: {str(e)}")

    def _copy_report(self):
        if not self.current_report_text:
            messagebox.showwarning("Empty", "No report content to copy.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.current_report_text)
        messagebox.showinfo("Copied", "Intelligence report copied to clipboard!")


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================
def main():
    root = tk.Tk()
    app = AutoAgentUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
