import os
import sys
import time
import math
import random
import threading
import tkinter as tk
from tkinter import ttk, messagebox

class AntiGravityAgentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IITM Pravartak Concept - Anti-Gravity Autonomous Agent")
        self.root.geometry("900x650")
        self.root.configure(bg="#1e1e2e")
        
        # Style setup
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background='#1e1e2e', foreground='#cdd6f4')
        self.style.configure('TProgressbar', thickness=20)
        
        # Agent Variables
        self.time_left = 10  # 5 minutes in seconds
        self.is_running = False
        
        # Simulation Parameters
        self.altitude = 0.0          # meters
        self.field_strength = 0.0    # %
        self.energy_used = 0.0       # %
        self.stability = 100.0       # %
        self.target_altitude = 100.0  # meters
        self.cycle_count = 0
        
        self.build_ui()
        
    def build_ui(self):
        # Header Control Panel
        control_frame = tk.Frame(self.root, bg="#252538", bd=1, relief=tk.RAISED)
        control_frame.pack(fill=tk.X, padx=15, pady=15)
        
        title_label = tk.Label(control_frame, text="LEVITY-BOT v1.0 (Autonomous Agent)", 
                               font=("Arial", 14, "bold"), bg="#252538", fg="#a6e3a1")
        title_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        self.start_btn = tk.Button(control_frame, text="Launch Autonomous Mission", 
                                   font=("Arial", 11, "bold"), bg="#a6e3a1", fg="#11111b",
                                   command=self.start_agent, padx=10, pady=5, relief=tk.FLAT)
        self.start_btn.pack(side=tk.RIGHT, padx=15, pady=10)
        
        # Main Layout: Left Status, Right Logs
        main_layout = tk.Frame(self.root, bg="#1e1e2e")
        main_layout.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        # Left Panel (Telemetry & Visuals)
        left_panel = tk.Frame(main_layout, bg="#1e1e2e", width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Countdown Timer Widget
        timer_frame = tk.Frame(left_panel, bg="#f38ba8", bd=0)
        timer_frame.pack(fill=tk.X, pady=(0, 15))
        self.timer_label = tk.Label(timer_frame, text="SAFETY TIMER: 05:00", 
                                    font=("Courier", 16, "bold"), bg="#f38ba8", fg="#11111b", pady=8)
        self.timer_label.pack()
        
        # Telemetry Box
        telemetry_frame = tk.LabelFrame(left_panel, text=" Live Telemetry ", font=("Arial", 11, "bold"),
                                        bg="#1e1e2e", fg="#cdd6f4", bd=2, relief=tk.GROOVE)
        telemetry_frame.pack(fill=tk.BOTH, expand=True)
        
        self.alt_var = tk.StringVar(value="Altitude: 0.00 m")
        self.field_var = tk.StringVar(value="Field Power: 0.00 %")
        self.energy_var = tk.StringVar(value="Energy Grid: 0.00 %")
        self.stab_var = tk.StringVar(value="Core Stability: 100.00 %")
        
        tk.Label(telemetry_frame, textvariable=self.alt_var, font=("Courier", 12, "bold"), bg="#1e1e2e", fg="#89b4fa").pack(anchor=tk.W, padx=15, pady=10)
        tk.Label(telemetry_frame, textvariable=self.field_var, font=("Courier", 12, "bold"), bg="#1e1e2e", fg="#fab387").pack(anchor=tk.W, padx=15, pady=10)
        tk.Label(telemetry_frame, textvariable=self.energy_var, font=("Courier", 12, "bold"), bg="#1e1e2e", fg="#f9e2af").pack(anchor=tk.W, padx=15, pady=10)
        tk.Label(telemetry_frame, textvariable=self.stab_var, font=("Courier", 12, "bold"), bg="#1e1e2e", fg="#a6e3a1").pack(anchor=tk.W, padx=15, pady=10)
        
        # Simple Canvas visualizer
        self.canvas = tk.Canvas(telemetry_frame, bg="#11111b", height=150, bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.X, padx=15, pady=15)
        # Draw platform
        self.box_id = self.canvas.create_rectangle(100, 110, 250, 140, fill="#f5e0dc", outline="#cdd6f4", width=2)
        self.canvas.create_line(0, 140, 350, 140, fill="#6c7086", width=2) # ground
        
        # Right Panel (Agent Thought Loop Logs)
        right_panel = tk.LabelFrame(main_layout, text=" Agent Operational Thought Loop (ReAct Framework) ", 
                                    font=("Arial", 11, "bold"), bg="#1e1e2e", fg="#cdd6f4", bd=2, relief=tk.GROOVE)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Text log with Scrollbar
        self.log_text = tk.Text(right_panel, font=("Courier", 10), bg="#11111b", fg="#cdd6f4", wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(right_panel, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.append_log("[System initialized. Agent sleeping. Press 'Launch Autonomous Mission' to start safely.]")

    def append_log(self, text, tag=None):
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, text + "")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def start_agent(self):
        if self.is_running:
            return
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED, text="Agent Running...", bg="#6c7086")
        
        # Start background threads so UI stays highly responsive
        threading.Thread(target=self.countdown_timer, daemon=True).start()
        threading.Thread(target=self.agent_loop, daemon=True).start()

    def countdown_timer(self):
        while self.time_left > 0 and self.is_running:
            mins, secs = divmod(self.time_left, 60)
            self.timer_label.config(text=f"SAFETY TIMER: {mins:02d}:{secs:02d}")
            time.sleep(1)
            self.time_left -= 1
            
        if self.time_left <= 0 and self.is_running:
            self.append_log("\n[CRITICAL SAFETY TRIGGER: 5 Minutes Hard Stop Reached! Forcing shutdown.]")
            self.stop_mission("5-Minute Safety Stop Triggered!")

    def agent_loop(self):
        self.append_log("\n>>> MISSION STARTED: Autonomously balancing cargo altitude using ReAct Pattern...")
        
        while self.is_running and self.time_left > 0:
            self.cycle_count += 1
            self.append_log(f"\n--- [CYCLE {self.cycle_count}] ---")
            
            # Step 1: THOUGHT
            self.append_log(f"THOUGHT: Evaluating current cargo state. Altitude is {self.altitude:.2f}m (Target: 100m). Grid energy used: {self.energy_used:.2f}%.")
            time.sleep(1.2) # Fast enough to see actions, slow enough to read
            
            # Agent logic: calculate adjustments needed
            if self.altitude < self.target_altitude:
                action_type = "Increase Anti-Gravity Field"
                # Add slight random noise to simulate dynamic real-world calculations
                adjustment = max(5.0, (self.target_altitude - self.altitude) * 0.2 + random.uniform(-2, 2))
                self.field_strength = min(100.0, self.field_strength + adjustment)
            else:
                action_type = "Calibrate and Reduce Field Strength to Hover"
                self.field_strength = max(30.0, self.field_strength - 4.0 + random.uniform(-1, 1))
                
            # Step 2: ACTION
            self.append_log(f"ACTION: Executing tool -> SetAntiGravityPower(Level={self.field_strength:.2f}%)")
            time.sleep(1.2)
            
            # Step 3: OBSERVATION (The environment reacts)
            # Simple physics simulation updates
            self.energy_used = min(100.0, self.energy_used + (self.field_strength * 0.08))
            
            # Calculate new altitude based on field power
            lift_force = self.field_strength * 0.15
            gravity_effect = 4.5
            net_movement = lift_force - gravity_effect
            self.altitude = max(0.0, self.altitude + net_movement)
            
            # Stability simulation
            if self.field_strength > 85.0:
                self.stability = max(50.0, self.stability - random.uniform(2, 8))
            else:
                self.stability = min(100.0, self.stability + random.uniform(1, 4))
                
            self.append_log(f"OBSERVATION: Environment reports platform altitude shifted by {net_movement:+.2f}m. Core stability at {self.stability:.1f}%.")
            
            # Update GUI elements safely on main thread
            self.root.after(0, self.update_telemetry_ui)
            
            # Goal check / Fail check rules
            if self.altitude >= self.target_altitude and self.stability >= 90.0:
                self.append_log("\n[SUCCESS: Core Target Met! Platform hovering stably at 100+ meters!]")
                self.stop_mission("Success! Target Stabilized.")
                break
                
            if self.energy_used >= 95.0:
                self.append_log("\n[WARNING: Energy Grid depleted above 95%! Autonomous safe emergency shutdown initiated.]")
                self.stop_mission("Emergency Grid Shutdown.")
                break
                
            time.sleep(1.5)

    def update_telemetry_ui(self):
        # Update text strings
        self.alt_var.set(f"Altitude: {self.altitude:.2f} m")
        self.field_var.set(f"Field Power: {self.field_strength:.2f} %")
        self.energy_var.set(f"Energy Grid: {self.energy_used:.2f} %")
        self.stab_var.set(f"Core Stability: {self.stability:.2f} %")
        
        # Animate the block rising on canvas
        # Max altitude (100m) maps to canvas y=20. Ground is y=110.
        pixel_lift = min(90, int(self.altitude * 0.9))
        current_y = 110 - pixel_lift
        
        self.canvas.coords(self.box_id, 100, current_y, 250, current_y + 30)

    def stop_mission(self, message):
        self.is_running = False
        self.root.after(0, lambda: messagebox.showinfo("Mission Status", f"Agent Stopped: {message}"))
        self.root.after(0, lambda: self.start_btn.config(text="Mission Ended", state=tk.DISABLED))

if __name__ == "__main__":
    root = tk.Tk()
    app = AntiGravityAgentApp(root)
    root.mainloop()
