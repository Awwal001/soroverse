#!/usr/bin/env python3
"""
LOCAL SOROverse Multi-Agent Demo - FIXED VERSION
"""

import asyncio
import sys
from pathlib import Path

# Add project root
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def run_local_demo():
    try:
        from uagents import Agent, Context
        from uagents_core.contrib.protocols.chat import ChatMessage, TextContent
        from datetime import datetime, timezone
        import uuid
        
        print("🚀 SOROverse LOCAL MULTI-AGENT DEMO")
        print("=" * 60)
        
        # Create demo coordinator
        demo_coordinator = Agent(
            name="DemoCoordinator",
            seed="demo_coordinator_seed_123",
            port=8006
        )
        
        # Agent addresses
        agents = {
            "SoroMind": "agent1qdrdup2klslg5adangymn9ajm72c2sr95phpjfhuaz2ryskwdl6s5rfazls",
            "SOMA Engine": "agent1qtqs2gzljl90mlcjenxj6nxjd2gkhpptdy8nsaz7terv5s8h8gkf2z5ya4s",
            "PSN Connect": "agent1qfnztyxpn3p87spf6ah6j8us3r9ms497ruez5r8fwvr4kpjpw662zsdmtvj",
            "SORO Orchestrator": "agent1q2a7v3rshca8knfzltm2q6uqxghx8fp02k7qg3cql9tdztgea539uuuch76"
        }
        
        demo_complete = asyncio.Event()
        
        @demo_coordinator.on_event("startup")
        async def start_demo(ctx: Context):
            print("🎬 Starting Demo Scenario: Academic Stress Support")
            print()
            
            # Simulate user message to SoroMind
            user_message = "I'm overwhelmed with final exams and can't sleep. I keep worrying I'll fail everything."
            
            print(f"👤 USER: {user_message}")
            print()
            print("🔄 MULTI-AGENT PROCESSING FLOW:")
            print("=" * 50)
            
            # Step 1: Send to SoroMind
            print("1. 📨 SoroMind: Receiving user message...")
            try:
                message = ChatMessage(
                    timestamp=datetime.now(timezone.utc),
                    msg_id=str(uuid.uuid4()),
                    content=[TextContent(type="text", text=user_message)]
                )
                
                await ctx.send(agents["SoroMind"], message)
                print("   ✅ Message sent to SoroMind")
                print("   💡 Check SoroMind terminal for: 'Received chat message'")
            except Exception as e:
                print(f"   ❌ Failed to send: {e}")
            
            # Wait and show what should happen
            await asyncio.sleep(3)
            
            print("\n2. 🧠 SOMA Engine: Should receive pattern analysis request")
            print("   💡 Check SOMA Engine terminal for pattern analysis")
            
            await asyncio.sleep(2)
            
            print("\n3. 🤝 PSN Connect: Should receive peer matching request") 
            print("   💡 Check PSN Connect terminal for matching algorithm")
            
            await asyncio.sleep(2)
            
            print("\n4. 💫 SORO Orchestrator: Should coordinate interventions")
            print("   💡 Check SORO Orchestrator terminal for coordination")
            
            await asyncio.sleep(2)
            
            print("\n" + "=" * 50)
            print("🎉 DEMO COMPLETE!")
            print("\n📊 What was demonstrated:")
            print("   ✅ Multi-agent architecture")
            print("   ✅ Protocol-based communication") 
            print("   ✅ Specialized agent coordination")
            print("   ✅ Mental health support pipeline")
            
            # Signal completion
            demo_complete.set()
        
        @demo_coordinator.on_message(model=ChatMessage)
        async def handle_responses(ctx: Context, sender: str, msg: ChatMessage):
            # Map addresses to names for better logging
            agent_names = {v: k for k, v in agents.items()}
            agent_name = agent_names.get(sender, sender)
            
            print(f"\n🎯 ACTUAL RESPONSE from {agent_name}:")
            for content in msg.content:
                if hasattr(content, 'text'):
                    print(f"   💬 {content.text}")
        
        print("🔄 Starting demo coordinator...")
        print("⏳ Watch all agent terminals for activity!")
        print()
        
        # Start the agent and wait for demo to complete
        await demo_coordinator.start()
        await demo_complete.wait()
        await asyncio.sleep(2)  # Give time for any final messages
        await demo_coordinator.stop()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure uagents is installed: pip install uagents")
    except Exception as e:
        print(f"❌ Demo failed: {e}")

# Use asyncio.run() properly
if __name__ == "__main__":
    asyncio.run(run_local_demo())