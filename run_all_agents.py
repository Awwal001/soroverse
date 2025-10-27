#!/usr/bin/env python3
"""
SOROverse Agent Launcher
"""

import subprocess
import time
import sys

AGENTS = [
    "agents/soromind_core.py",
    "agents/soma_engine.py", 
    "agents/soro_orchestrator.py",
    "agents/psn_connect.py"
]

processes = []

def main():
    print("🧠 SOROverse Multi-Agent System")
    print("=" * 40)
    
    for agent_file in AGENTS:
        try:
            print(f"🚀 Starting {agent_file}...")
            process = subprocess.Popen([sys.executable, agent_file])
            processes.append(process)
            time.sleep(2)
        except Exception as e:
            print(f"❌ Failed to start {agent_file}: {e}")
    
    print("\n✅ All agents started successfully")
    print("Press Ctrl+C to stop all agents")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping all agents...")
        for process in processes:
            process.terminate()

if __name__ == "__main__":
    main()
