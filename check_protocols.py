#!/usr/bin/env python3
"""
Check what protocols are actually active on each agent
"""

import requests
import json

def check_agent_protocols():
    agents = [
        ("SoroMind", 8001, "agent1qdrdup2klslg5adangymn9ajm72c2sr95phpjfhuaz2ryskwdl6s5rfazls"),
        ("SOMA Engine", 8002, "agent1qtqs2gzljl90mlcjenxj6nxjd2gkhpptdy8nsaz7terv5s8h8gkf2z5ya4s"),
        ("SORO Orchestrator", 8003, "agent1q2a7v3rshca8knfzltm2q6uqxghx8fp02k7qg3cql9tdztgea539uuuch76"),
        ("PSN Connect", 8004, "agent1qfnztyxpn3p87spf6ah6j8us3r9ms497ruez5r8fwvr4kpjpw662zsdmtvj")
    ]
    
    print("🔍 Checking Active Protocols...")
    print("=" * 50)
    
    for name, port, address in agents:
        print(f"\n🧠 {name} (Port {port}):")
        print(f"   Address: {address}")
        
        # Check if agent is responding
        try:
            response = requests.get(f"http://127.0.0.1:{port}/submit", timeout=5)
            print(f"   Status: ✅ HTTP {response.status_code}")
            
            # Try to get any available info
            if response.status_code == 200:
                print(f"   Response: {response.text[:100]}...")
                
        except requests.exceptions.ConnectionError:
            print(f"   Status: ❌ Not responding")
        except Exception as e:
            print(f"   Status: ⚠️  Error - {e}")

if __name__ == "__main__":
    check_agent_protocols()