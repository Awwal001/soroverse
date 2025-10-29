#!/usr/bin/env python3
"""
SOROverse Agent Launcher - Fixed for virtual environment
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get the path to the current Python executable in the virtual environment
venv_python = sys.executable

AGENTS = [
    {"name": "SoroMind Core", "file": "agents/soromind_core.py", "port": 8001},
    {"name": "SOMA Engine", "file": "agents/soma_engine.py", "port": 8002},
    {"name": "SORO Orchestrator", "file": "agents/soro_orchestrator.py", "port": 8003},
    {"name": "PSN Connect", "file": "agents/psn_connect.py", "port": 8004}
]

processes = []

def start_agent(agent_config):
    """Start a single agent using the virtual environment Python"""
    try:
        print(f"🚀 Starting {agent_config['name']}...")
        
        # Use the virtual environment Python executable
        process = subprocess.Popen([
            venv_python, 
            agent_config['file']
        ])
        
        processes.append(process)
        time.sleep(3)  # Give more time for agent to start
        return True
        
    except Exception as e:
        print(f"❌ Failed to start {agent_config['name']}: {e}")
        return False

def stop_agents():
    """Stop all running agents"""
    print("\n🛑 Stopping all agents...")
    for process in processes:
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            process.kill()
    processes.clear()

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    stop_agents()
    sys.exit(0)

def verify_environment():
    """Verify that we're in the right environment"""
    print("🔍 Verifying environment...")
    
    # Check if we're in virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in virtual environment")
    else:
        print("⚠️  Not running in virtual environment")
    
    # Check required environment variables
    required_vars = ['ASI_API_KEY', 'AGENTVERSE_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or f"your_{var.lower()}" in value:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Please configure in .env: {', '.join(missing_vars)}")
        return False
    
    print("✅ Environment variables configured")
    return True

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    print("🧠 SOROverse Multi-Agent System")
    print("=" * 50)
    
    # Verify environment first
    if not verify_environment():
        print("\n💡 Please configure your .env file with actual API keys")
        return
    
    print(f"🐍 Using Python: {venv_python}")
    print(f"📁 Project root: {Path.cwd()}")
    
    # Start all agents
    successful_starts = 0
    for agent in AGENTS:
        if start_agent(agent):
            successful_starts += 1
    
    print(f"\n✅ {successful_starts}/{len(AGENTS)} agents started successfully")
    
    if successful_starts > 0:
        print("\n🌐 Agent Addresses:")
        print("• SoroMind Core: agent1q2w... (User Interface)")
        print("• SOMA Engine: agent1q3e... (Pattern Analysis)") 
        print("• SORO Orchestrator: agent1q4r... (Intervention Coordination)")
        print("• PSN Connect: agent1q5t... (Peer Matching)")
        
        print("\n🔗 Next: Connect to Agentverse and enable Mailbox")
        print("💬 Test with ASI:One at https://asi1.ai")
        print("\nPress Ctrl+C to stop all agents")
    else:
        print("💥 No agents started successfully")
        return
    
    # Keep running until interrupted
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_agents()

if __name__ == "__main__":
    main()