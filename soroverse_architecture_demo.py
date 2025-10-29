#!/usr/bin/env python3
"""
SOROverse Architecture Demo - Shows Multi-Agent Coordination
"""

import time
import threading
from datetime import datetime

class AgentSimulator:
    """Simulates agent activity for demo purposes"""
    
    def __init__(self, name, port, address):
        self.name = name
        self.port = port
        self.address = address
        self.messages_received = []
    
    def receive_message(self, message, from_agent=""):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.messages_received.append({
            'timestamp': timestamp,
            'from': from_agent,
            'message': message
        })
        print(f"🕒 {timestamp} | 📨 {self.name} received: {message}")
        return f"{self.name} processed: {message}"

class SOROverseDemo:
    """Main demo coordinator"""
    
    def __init__(self):
        print("🚀 SOROverse Multi-Agent System Demo")
        print("=" * 60)
        
        # Create simulated agents
        self.agents = {
            "SoroMind Core": AgentSimulator("SoroMind Core", 8001, "agent1qdrdup2klslg5adangymn9ajm72c2sr95phpjfhuaz2ryskwdl6s5rfazls"),
            "SOMA Engine": AgentSimulator("SOMA Engine", 8002, "agent1qtqs2gzljl90mlcjenxj6nxjd2gkhpptdy8nsaz7terv5s8h8gkf2z5ya4s"),
            "PSN Connect": AgentSimulator("PSN Connect", 8004, "agent1qfnztyxpn3p87spf6ah6j8us3r9ms497ruez5r8fwvr4kpjpw662zsdmtvj"),
            "SORO Orchestrator": AgentSimulator("SORO Orchestrator", 8003, "agent1q2a7v3rshca8knfzltm2q6uqxghx8fp02k7qg3cql9tdztgea539uuuch76")
        }
    
    def demo_academic_stress_scenario(self):
        """Demo Scenario 1: Academic Stress Support"""
        print("\n🎓 DEMO SCENARIO 1: Academic Stress Support")
        print("=" * 50)
        
        user_message = "I'm overwhelmed with final exams and can't sleep. I keep worrying I'll fail everything."
        
        print(f"👤 USER: {user_message}")
        print("\n🔄 MULTI-AGENT COORDINATION:")
        print("-" * 40)
        
        # Step 1: User message to SoroMind
        time.sleep(2)
        soromind_response = self.agents["SoroMind Core"].receive_message(
            user_message, "User"
        )
        print("   🔍 SoroMind: Crisis detection - Medium risk detected")
        print("   💬 SoroMind: 'I hear you're feeling overwhelmed. Let me help.'")
        
        # Step 2: SoroMind to SOMA Engine for pattern analysis
        time.sleep(2)
        soma_response = self.agents["SOMA Engine"].receive_message(
            "Pattern analysis: academic stress, perfectionism, sleep issues",
            "SoroMind Core"
        )
        print("   🧠 SOMA Engine: Analyzing cognitive patterns...")
        print("   📊 Detected: Perfectionism (85%), Catastrophizing (72%), Sleep disruption")
        
        # Step 3: SoroMind to PSN Connect for peer support
        time.sleep(2)
        psn_response = self.agents["PSN Connect"].receive_message(
            "Peer match: academic stress, evening availability, medium urgency",
            "SoroMind Core"
        )
        print("   🤝 PSN Connect: Finding matching peer supporters...")
        print("   👥 Found 3 matches: Alex (4.8★), Taylor (4.6★), Jordan (4.7★)")
        
        # Step 4: SORO Orchestrator coordinates interventions
        time.sleep(2)
        orchestrator_response = self.agents["SORO Orchestrator"].receive_message(
            "Coordinate: mindfulness + peer support + study techniques",
            "SoroMind Core"
        )
        print("   💫 SORO Orchestrator: Coordinating multi-modal intervention...")
        print("   🎯 Strategy: Mindfulness + Peer support + Time management")
        
        # Final response
        time.sleep(2)
        print("\n💬 SoroMind Final Response to User:")
        print("   'I understand how overwhelming exams can be. Based on our analysis:")
        print("   • Try the 4-7-8 breathing technique when feeling anxious")
        print("   • Connect with Alex who specializes in academic stress")
        print("   • Break study sessions into 25-minute focused blocks")
        print("   • Remember that perfection isn't required for success'")
    
    def demo_work_anxiety_scenario(self):
        """Demo Scenario 2: Work Anxiety"""
        print("\n💼 DEMO SCENARIO 2: Work Anxiety & Imposter Syndrome")
        print("=" * 50)
        
        user_message = "I have a big presentation tomorrow and I'm terrified. I feel like everyone will realize I'm not qualified."
        
        print(f"👤 USER: {user_message}")
        print("\n🔄 MULTI-AGENT COORDINATION:")
        print("-" * 40)
        
        # Step 1: User message to SoroMind
        time.sleep(2)
        self.agents["SoroMind Core"].receive_message(user_message, "User")
        print("   🔍 SoroMind: Detecting imposter syndrome + presentation anxiety")
        print("   💬 SoroMind: 'Presentation anxiety is completely normal. Let's work through this.'")
        
        # Step 2: Pattern analysis
        time.sleep(2)
        self.agents["SOMA Engine"].receive_message(
            "Pattern analysis: imposter syndrome, performance anxiety, fear of judgment",
            "SoroMind Core"
        )
        print("   🧠 SOMA Engine: Cognitive pattern analysis...")
        print("   📊 Detected: Imposter syndrome (78%), Performance anxiety (82%)")
        
        # Step 3: Peer matching
        time.sleep(2)
        self.agents["PSN Connect"].receive_message(
            "Peer match: work anxiety, imposter syndrome, immediate support",
            "SoroMind Core"
        )
        print("   🤝 PSN Connect: Matching with experienced professionals...")
        print("   👥 Taylor available now - specializes in workplace anxiety")
        
        # Step 4: Intervention coordination
        time.sleep(2)
        self.agents["SORO Orchestrator"].receive_message(
            "Coordinate: CBT techniques + peer support + preparation strategies",
            "SoroMind Core"
        )
        print("   💫 SORO Orchestrator: Deploying evidence-based interventions...")
        print("   🎯 Strategy: CBT reframing + Peer validation + Practical prep")
        
        # Final response
        time.sleep(2)
        print("\n💬 SoroMind Final Response to User:")
        print("   'Many successful people experience imposter syndrome. Here's what can help:")
        print("   • Reframe thoughts: 'I'm prepared and capable'")
        print("   • Connect with Taylor who overcame similar challenges'")
        print("   • Practice your presentation out loud 3 times")
        print("   • Remember: The audience wants you to succeed'")
    
    def show_architecture(self):
        """Show the system architecture"""
        print("\n🏗️ SOROverse SYSTEM ARCHITECTURE")
        print("=" * 50)
        
        print("🔗 Agent Network:")
        for name, agent in self.agents.items():
            print(f"   • {name} (Port {agent.port})")
            print(f"     Address: {agent.address[:20]}...")
        
        print("\n🔄 Communication Flow:")
        print("   👤 User → SoroMind Core → SOMA Engine → PSN Connect → SORO Orchestrator")
        
        print("\n🎯 Agent Responsibilities:")
        print("   • SoroMind Core: User interface & crisis detection")
        print("   • SOMA Engine: Pattern analysis & cognitive mapping") 
        print("   • PSN Connect: Peer matching & community coordination")
        print("   • SORO Orchestrator: Multi-agent intervention coordination")
    
    def run_complete_demo(self):
        """Run the complete demo"""
        print("🎬 Starting SOROverse Live Demo")
        print("Note: Real agents are running on ports 8001-8004")
        print("This simulation shows the coordination that happens between them")
        print()
        
        # Show architecture
        self.show_architecture()
        time.sleep(3)
        
        # Run demo scenarios
        self.demo_academic_stress_scenario()
        time.sleep(3)
        
        self.demo_work_anxiety_scenario()
        
        # Summary
        print("\n" + "=" * 60)
        print("🎉 DEMO COMPLETE!")
        print("\n📊 Real System Status:")
        print("   ✅ 4 uAgents running locally on ports 8001-8004")
        print("   ✅ Multi-agent architecture implemented")
        print("   ✅ Protocol-based communication ready")
        print("   ✅ MeTTa knowledge graph integrated")
        print("   ⚠️  Agentverse registration pending (funding issue)")
        
        print("\n🚀 Next Steps:")
        print("   • Get testnet funds for Agentverse registration")
        print("   • Deploy to Agentverse for global access")
        print("   • Connect via ASI:One for live chatting")

if __name__ == "__main__":
    demo = SOROverseDemo()
    demo.run_complete_demo()