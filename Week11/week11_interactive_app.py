import streamlit as st
import time
import random
import pandas as pd
import json

st.set_page_config(
    page_title="Week 11: Decision Making & Planning in Agents",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Learner-Friendly Interface
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .concept-card {
        background-color: #F8FAFC;
        border-left: 5px solid #3B82F6;
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .alert-card {
        background-color: #FEF2F2;
        border-left: 5px solid #EF4444;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .success-card {
        background-color: #F0FDF4;
        border-left: 5px solid #22C55E;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .metric-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        border-radius: 6px 6px 0px 0px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎓 Week 11: Decision Making & Planning in Agents</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive Learning Sandbox & Simulation Studio • IIT Madras Agentic AI Programme</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=80)
st.sidebar.title("Navigation & Controls")
module = st.sidebar.radio(
    "Choose Learning Module:",
    [
        "1. 🎯 Goal Pipeline Simulator",
        "2. ⚔️ Planning Arena (Hierarchical vs Reactive vs Hybrid)",
        "3. 👥 Multi-Agent Coordination (Conductor vs Kitchen)",
        "4. 🔄 Reinforcement Feedback Loops",
        "5. 📝 Interactive MCQs & Capstone Test",
        "6. 📓 View Handwritten Notebook"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**💡 Lecture Blueprint:**
- **Topic 1:** Goal-Setting in Agents
- **Topic 2:** Real-World Applications (Triage)
- **Topic 3:** Hierarchical vs Reactive
- **Topic 4:** Planning in Action
- **Topic 5:** Hybrid Production Agents
- **Topic 6:** Multi-Agent Coordination
- **Topic 7:** Reinforcement Loops
""")

# ==========================================
# MODULE 1: GOAL PIPELINE SIMULATOR
# ==========================================
if "1. 🎯 Goal Pipeline Simulator" in module:
    st.subheader("🎯 Module 1: The Goal Execution Pipeline")
    st.markdown("""
    In autonomous agents, instructions are converted into actionable intelligence via the 4-stage pipeline:
    **Goal $\\rightarrow$ Decompose $\\rightarrow$ Execute $\\rightarrow$ Reflect** (Slides 5–9).
    """)

    scenario = st.selectbox(
        "Select a Real-World Scenario:",
        [
            "Hospital Emergency Room Triage (Slide 13-23)",
            "Financial Investment Research Agent (Slide 12)",
            "Autonomous Delivery Drone (Slide 48-52)"
        ]
    )

    if scenario == "Hospital Emergency Room Triage (Slide 13-23)":
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("### 📋 Input Patient Data")
            hr = st.slider("Heart Rate (BPM)", min_value=40, max_value=180, value=115)
            spo2 = st.slider("Oxygen Saturation (SpO2 %)", min_value=70, max_value=100, value=91)
            pain = st.slider("Pain Score (1-10)", min_value=1, max_value=10, value=8)
            sudden_crash = st.checkbox("🚨 Inject Dynamic Disruption (Vitals crash while waiting)", value=False)
            
            run_btn = st.button("🚀 Run Goal Execution Pipeline", type="primary")

        with col2:
            st.markdown("### 🔄 Pipeline Execution Visualizer")
            if run_btn or sudden_crash:
                # Stage 1: Goal
                st.markdown("""
                <div class="concept-card">
                    <strong>Step 1: Goal Specification</strong><br>
                    • <em>Primary Goal:</em> Support clinical decision-making & risk triage.<br>
                    • <em>Ethical Boundary:</em> Human-in-the-Loop (Doctor must approve prescription).<br>
                    • <em>SLA:</em> Triage within &lt; 90 seconds.
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.3)

                # Stage 2: Decompose
                st.markdown("""
                <div class="concept-card">
                    <strong>Step 2: Hierarchical Task Decomposition</strong><br>
                    ├─ Subtask 1: Parse vital telemetry streams<br>
                    ├─ Subtask 2: Match against Emergency Severity Index (ESI)<br>
                    └─ Subtask 3: Allocate ED Bed & Alert Specialist
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.3)

                # Stage 3: Execute
                if sudden_crash or spo2 < 88 or hr > 140:
                    st.markdown("""
                    <div class="alert-card">
                        <strong>Step 3: Action Execution (REACTIVE INTERRUPT!)</strong><br>
                        ⚠️ Critical Anomaly Detected! SpO2 collapsed to Critical Level.<br>
                        <strong>Agent Action:</strong> Instantly escalated to <strong>ESI Level 1 (Resuscitation)</strong>.<br>
                        Autonomous Code Blue alert dispatched to ED attending physician!
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="success-card">
                        <strong>Step 3: Action Execution (Standard Path)</strong><br>
                        Patient categorized as <strong>ESI Level 2 (Emergent)</strong> based on HR={hr} and Pain={pain}.<br>
                        Preliminary diagnostic panel (ECG, Trop-I) queued for physician sign-off.
                    </div>
                    """, unsafe_allow_html=True)
                time.sleep(0.3)

                # Stage 4: Reflect
                st.markdown("""
                <div class="concept-card" style="border-left-color: #10B981;">
                    <strong>Step 4: Reflection & Reinforcement Loop</strong><br>
                    • Evaluated triage latency: <strong>42 ms</strong> (Well within SLA).<br>
                    • Success Criteria Met: Doctor confirmed recommendation with zero override delay.<br>
                    • Episodic Memory updated: +1 positive reinforcement to vitals risk weights.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Adjust the patient vitals and click **Run Goal Execution Pipeline** to see the pipeline in action!")

    elif scenario == "Financial Investment Research Agent (Slide 12)":
        st.markdown("""
        <div class="concept-card">
            <strong>Goal:</strong> Formulate buy/hold/sell report on Tech Sector under volatility.<br>
            <strong>Decomposition:</strong> Subtask 1: Ingest SEC filings $\\rightarrow$ Subtask 2: Query live market APIs $\\rightarrow$ Subtask 3: Quantify risk metrics $\\rightarrow$ Subtask 4: Draft thesis.<br>
            <strong>Execution:</strong> Parallel retrieval using tool-calling.<br>
            <strong>Reflection:</strong> Cross-checks market metrics against analyst consensus to ensure no hallucination.
        </div>
        """, unsafe_allow_html=True)
        st.success("Financial agent pipeline ready for integration.")

    elif scenario == "Autonomous Delivery Drone (Slide 48-52)":
        st.markdown("""
        <div class="concept-card">
            <strong>Goal:</strong> Deliver medical insulin vial to designated rooftop landing pad.<br>
            <strong>Decomposition:</strong> Global GPS Waypoint Generation $\\rightarrow$ Air Traffic Clearance $\\rightarrow$ Descent protocol.<br>
            <strong>Dynamic Event:</strong> Wind gust or temporary no-fly restriction.<br>
            <strong>Reflection:</strong> Post-flight battery consumption vs estimated burn model update.
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# MODULE 2: PLANNING ARENA (HIERARCHICAL VS REACTIVE VS HYBRID)
# ==========================================
elif "2. ⚔️ Planning Arena" in module:
    st.subheader("⚔️ Module 2: The Planning Arena: Hierarchical vs. Reactive vs. Hybrid")
    st.markdown("""
    Compare how the **three core agent planning architectures** behave when the environment throws unexpected surprises!
    *(Reference: Slides 24–48)*
    """)

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("### ⚙️ Environment Configuration")
        env_complexity = st.select_slider(
            "Environmental Turbulence / Uncertainty:",
            options=["Low (Predictable like Italy Itinerary)", "Medium (City Traffic)", "Extreme (Burning Building)"],
            value="Medium (City Traffic)"
        )
        
        inject_obstacle = st.checkbox("🚧 Introduce Roadblock / Sudden Obstacle", value=True)
        max_detour_allowance = st.slider("Hybrid Arbitration Threshold (Allowed detour km before replan)", 1, 10, 3)

        st.markdown("### 📊 Agent Architectural Profiles")
        st.markdown("""
        - 🏛️ **Hierarchical Agent (Planner):** Top-down, deep lookahead, optimal under static conditions, but blind to sudden changes.
        - ⚡ **Reactive Agent (Reflex):** Fast stimulus-response (`IF blocked THEN turn`), no long-term memory, prone to loops.
        - 🚀 **Hybrid Agent (Production):** Hierarchical global navigation + reactive obstacle reflex + arbitration replanner!
        """)
        
        simulate_btn = st.button("🏁 Run Planning Arena Simulation", type="primary")

    with col2:
        st.markdown("### 🏁 Live Simulation Results")
        if simulate_btn:
            with st.spinner("Simulating multi-step execution..."):
                time.sleep(0.5)

            st.write("#### 1. 🏛️ Purely Hierarchical Agent")
            if inject_obstacle:
                st.error("❌ **MISSION FAILED / STALLED!**")
                st.caption("Agent rigidly followed its precomputed 5-step path. When roadblock was encountered, it had no reflex mechanism to step aside. Execution halted awaiting manual override.")
            else:
                st.success("✅ **MISSION SUCCESS!** Optimal path followed with minimal resource burn.")

            st.write("#### 2. ⚡ Purely Reactive Agent")
            if inject_obstacle:
                st.warning("⚠️ **SUB-OPTIMAL / WANDERING!**")
                st.caption("Agent easily dodged the roadblock using instant reflex (`turn_right()`), but lacking a global goal map, it drifted into dead-end streets and wasted 4x more energy.")
            else:
                st.info("ℹ️ Reached destination, but took zig-zag meandering route due to local noise.")

            st.write("#### 3. 🚀 Hybrid Agent (Hierarchical + Reactive + Arbitration)")
            st.success("🎉 **OPTIMAL MISSION SUCCESS!**")
            st.markdown(f"""
            - **Global Planner:** Formulated baseline path A $\\rightarrow$ B.
            - **Reactive Layer:** Instantly detected roadblock, initiated local evasive maneuver without waiting.
            - **Arbitration Engine:** Measured detour = 2.4 km (Threshold = {max_detour_allowance} km).
            - *Detour &le; Threshold:* Patched local trajectory and resumed global plan seamlessly!
            """)

            # Comparison Table
            st.markdown("### 📈 Quantitative Performance Comparison")
            df = pd.DataFrame({
                "Architecture": ["Hierarchical Only", "Reactive Only", "Hybrid Agent"],
                "Response Latency": ["High (500-1500ms)", "Ultra-Low (<10ms)", "Adaptive (10ms reflex / 400ms replan)"],
                "Global Optimality": ["High (if static)", "Poor (Myopic)", "High (Adaptive)"],
                "Robustness to Disruption": ["Very Low (Brittle)", "High (Fluid)", "Very High (Production Standard)"]
            })
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Click **Run Planning Arena Simulation** to benchmark the 3 agents side by side.")

# ==========================================
# MODULE 3: MULTI-AGENT COORDINATION
# ==========================================
elif "3. 👥 Multi-Agent Coordination" in module:
    st.subheader("👥 Module 3: Multi-Agent Planning Strategies")
    st.markdown("""
    Explore how agents collaborate at scale: **Centralized Coordinator (Orchestra Conductor)** vs. **Decentralized / Cooperative (Restaurant Kitchen)**.
    *(Reference: Slides 54–65)*
    """)

    arch_mode = st.radio(
        "Choose Coordination Architecture:",
        ["Centralized Planning (The Orchestra Conductor)", "Decentralized / Cooperative Planning (The Restaurant Kitchen)"],
        horizontal=True
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        agent_count = st.slider("Number of Operational Sub-Agents (N)", min_value=3, max_value=50, value=8)
        crash_coordinator = st.checkbox("💥 Simulate Central Coordinator Crash / Network Partition", value=False)
        sim_run = st.button("🚀 Simulate Multi-Agent System")

    with col2:
        if sim_run or crash_coordinator:
            if "Centralized" in arch_mode:
                st.markdown("### 🎼 Centralized Coordinator Architecture")
                if crash_coordinator:
                    st.error("🚨 **SYSTEM OUTAGE! Single Point of Failure (SPOF) Triggered!**")
                    st.write(f"The Central Master Node went offline. All {agent_count} worker agents are frozen idle because no task assignments can be issued.")
                    st.metric("Total Messages Exchanged", "0 (Blocked)")
                    st.metric("System Throughput", "0%")
                else:
                    msgs = agent_count * 2
                    st.success("🟢 **GLOBAL CONSISTENCY MAINTAINED**")
                    st.write(f"Central Coordinator smoothly scheduled tasks across all {agent_count} workers with zero conflicting assignments.")
                    st.metric("Message Complexity", f"O(N) = {msgs} messages")
                    st.metric("Conflict Rate", "0%")
            else:
                st.markdown("### 🍳 Decentralized Cooperative Architecture")
                if crash_coordinator:
                    st.success("🛡️ **FAULT-TOLERANT! Resilient Peer-to-Peer Operation!**")
                    st.write("Even though one central gateway failed, the agents used peer-to-peer gossip & auction protocols to redistribute pending tasks among themselves!")
                else:
                    st.info("🤝 **PEER COOPERATION ACTIVE**")
                
                # O(N^2) message calculation
                peer_msgs = agent_count * (agent_count - 1)
                st.metric("Message Complexity", f"O(N²) = {peer_msgs} messages")
                if agent_count > 25:
                    st.warning("⚠️ High network overhead! Peer-to-peer chatter is consuming substantial bandwidth.")
                else:
                    st.success("Network traffic is manageable for this swarm size.")
        else:
            st.info("Select parameters and click **Simulate Multi-Agent System**.")

# ==========================================
# MODULE 4: REINFORCEMENT FEEDBACK LOOPS
# ==========================================
elif "4. 🔄 Reinforcement Feedback Loops" in module:
    st.subheader("🔄 Module 4: Reinforcement Loops (Static Plans vs. Living Processes)")
    st.markdown("""
    Slide 75: *\"Static plans assume the world does not change; Reinforcement loops turn plans into living processes.\"*
    Watch an autonomous agent refine its heuristic weights across multiple iterations.
    """)

    iterations = st.slider("Simulate Number of Planning Episodes:", min_value=1, max_value=10, value=5)
    
    if st.button("Run Adaptive Learning Loop"):
        history = []
        base_error = 80
        for ep in range(1, iterations + 1):
            error = max(5, int(base_error * (0.6 ** (ep - 1)) + random.randint(-4, 4)))
            reward = 100 - error
            history.append({
                "Episode": f"Run #{ep}",
                "Planning Accuracy (%)": min(99, reward),
                "Execution Deviation (ms)": error * 10,
                "Policy Status": "Refining Weights" if ep < iterations else "Converged / Optimized"
            })
        
        hist_df = pd.DataFrame(history)
        st.table(hist_df)
        st.line_chart(hist_df.set_index("Episode")["Planning Accuracy (%)"])
        st.success("🎉 Agent demonstrated policy improvement via post-action reflection!")

# ==========================================
# MODULE 5: INTERACTIVE MCQS & CAPSTONE TEST
# ==========================================
elif "5. 📝 Interactive MCQs & Capstone Test" in module:
    st.subheader("📝 Module 5: Test Your Mastery (IITM Exam-Grade MCQs)")
    st.markdown("Select your answers to see instant explanations and grading.")

    # Question 1
    st.markdown("#### **Q1: Planning Paradigms in Dynamic Environments**")
    q1 = st.radio(
        "A firefighting robot is entering a collapsing chemical warehouse with high thermal variance and unpredictable rubble falls. What architecture is most suitable?",
        [
            "Pure Hierarchical Planning (Calculate the complete exit route prior to entry)",
            "Pure Reactive Planning (Rely solely on bumper bump sensors with zero map memory)",
            "Hybrid Planning (Maintain top-level facility map while using real-time reflex loops for falling debris)",
            "Static Batch Scripting (Follow hardcoded coordinates without sensory input)"
        ],
        index=None
    )
    if q1:
        if "Hybrid Planning" in q1:
            st.success("✅ **Correct!** Slide 47 explains that hybrid agents combine global hierarchical direction with reactive reflexes to handle immediate physical peril.")
        else:
            st.error("❌ **Incorrect.** Pure hierarchical plans will freeze upon unexpected rubble, while pure reactive agents get lost without an exit map.")

    st.markdown("---")

    # Question 2
    st.markdown("#### **Q2: Multi-Agent Scaling Trade-offs**")
    q2 = st.radio(
        "What is the primary architectural vulnerability of a Centralized Coordinator ('The Orchestra Conductor') in high-frequency multi-agent trading systems?",
        [
            "High message complexity of O(N²)",
            "Single Point of Failure (SPOF) and processing bottleneck at the central coordinator node",
            "Inability to optimize global objectives",
            "Agents refuse to execute deterministic instructions"
        ],
        index=None
    )
    if q2:
        if "Single Point of Failure" in q2:
            st.success("✅ **Correct!** Slide 58 highlights that if the central master node crashes or is throttled, the entire ecosystem stalls.")
        else:
            st.error("❌ **Incorrect.** Centralized systems have low message complexity O(N), but suffer from single point of failure.")

    st.markdown("---")

    # Final Capstone Question
    st.markdown("### 🏆 The Final Capstone Litmus Test")
    st.info("""
    **If you can articulate this answer in your viva/exam, you have mastered Week 11:**
    *\"How do you architect a hybrid, multi-agent dispatch system for hospital emergency response that maintains long-term operational plans while reactively handling critical real-time disruptions (e.g., patient condition crashes, road closures, or ICU bed shortages), and how does the feedback loop adapt future plans?\"*
    """)
    with st.expander("🔍 Click to reveal the Model Architecture Solution"):
        st.markdown("""
        **1. Goal Hierarchy:**
        - Top Goal: Minimize mortality and ED wait times.
        - Decomposed Sub-Goals: Triage classification $\\rightarrow$ Route optimization $\\rightarrow$ Resource pre-allocation.
        
        **2. Arbitration Layer:**
        - If minor delay (&lt; 5 mins): Keep original plan and apply reactive speed adjust.
        - If major disruption (ICU full or cardiac arrest en route): Invalidate current sub-plan, trigger dynamic replan to redirect to alternate trauma center.

        **3. Multi-Agent Coordination:**
        - Centralized coordinator for global ED bed tracking.
        - Decentralized peer-to-peer relay between ambulances when local networks disconnect.

        **4. Reinforcement Loop:**
        - Log actual transit times vs predicted times to adjust routing heuristics in dynamic memory.
        """)

# ==========================================
# MODULE 6: VIEW HANDWRITTEN NOTEBOOK
# ==========================================
elif "6. 📓 View Handwritten Notebook" in module:
    st.subheader("📓 Module 6: Week 11 Handwritten Student Notebook")
    st.markdown("""
    Here is the complete, beautifully styled handwritten study notebook covering all 7 lecture topics, exam alerts, and mental models!
    You can also open the file directly in your browser: [Week11_Handwritten_Notebook.html](file:///C:/Users/Maharshi/Documents/IITM_Agentic/Week11/Week11_Handwritten_Notebook.html).
    """)

    try:
        with open(r"C:\Users\Maharshi\Documents\IITM_Agentic\Week11\Week11_Handwritten_Notebook.html", "r", encoding="utf-8") as f:
            notebook_html = f.read()
        st.components.v1.html(notebook_html, height=1200, scrolling=True)
    except Exception as e:
        st.error(f"Error loading notebook: {e}")
