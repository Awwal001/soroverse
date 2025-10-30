#!/usr/bin/env python3
"""
PSN Connect - COMPLETE FIXED VERSION
"""

import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any
from uagents import Agent, Context, Protocol

# Import COMMON models
from common_models import PeerSupportRecommendation, PeerSupportActivation

print("✅ PSN Connect - Common models imported")

# Agent addresses
SORO_ORCHESTRATOR_ADDRESS = "agent1q2a7v3rshca8knfzltm2q6uqxghx8fp02k7qg3cql9tdztgea539uuuch76"

# Databases
PEER_SUPPORTERS = [
    {'id': 'peer_001', 'name': 'Alex', 'expertise': ['academic_stress', 'anxiety'], 'rating': 4.8},
    {'id': 'peer_002', 'name': 'Taylor', 'expertise': ['work_anxiety', 'career'], 'rating': 4.6},
    {'id': 'peer_003', 'name': 'Jordan', 'expertise': ['relationship_issues', 'loneliness'], 'rating': 4.7}
]

GROUP_SESSIONS = [
    {'id': 'group_001', 'topic': 'Academic Stress Management', 'schedule': 'Mondays 6 PM'},
    {'id': 'group_002', 'topic': 'Anxiety Support Circle', 'schedule': 'Tues/Thurs 7 PM'}
]

# Agent
psn_connect = Agent(
    name="PSN Connect",
    seed=os.getenv("PSN_CONNECT_SEED", "psn_connect_secret_phrase_004"),
    port=8003,
    endpoint=["http://localhost:8003/submit"],
    mailbox=False
)

print("=" * 60)
print("🤝 PSN CONNECT - FIXED WITH COMMON MODELS")
print("=" * 60)
print(f"📍 Agent Address: {psn_connect.address}")

# Protocol
peer_match_proto = Protocol(name="PeerSupportMatching", version="1.1.0")

@peer_match_proto.on_message(PeerSupportRecommendation)
async def handle_orchestrator_recommendation(ctx: Context, sender: str, msg: PeerSupportRecommendation):
    print(f"💫 PSN: RECEIVED from Orchestrator!")
    print(f"   👤 User: {msg.user_id[:8]}...")
    print(f"   🎯 Support: {msg.recommended_support_type}")
    print(f"   🔍 Patterns: {msg.patterns}")
    print(f"   ⚠️ Urgency: {msg.urgency}")
    print(f"   📊 Confidence: {msg.orchestrator_confidence}")
    
    try:
        # Find matching peers
        matched_peers = []
        for peer in PEER_SUPPORTERS:
            if any(pattern in str(peer['expertise']) for pattern in msg.patterns):
                matched_peers.append({
                    'id': peer['id'],
                    'name': peer['name'], 
                    'expertise': peer['expertise'],
                    'match_reason': f"Expert in {', '.join(peer['expertise'][:2])}"
                })
                if len(matched_peers) >= 2:
                    break
        
        # Find relevant groups
        relevant_groups = []
        for group in GROUP_SESSIONS:
            if any(pattern in group['topic'].lower() for pattern in msg.patterns):
                relevant_groups.append({
                    'id': group['id'],
                    'topic': group['topic'],
                    'schedule': group['schedule']
                })
                if len(relevant_groups) >= 2:
                    break
        
        # Send activation back to orchestrator
        activation = PeerSupportActivation(
            session_id=str(uuid.uuid4()),
            user_id=msg.user_id,
            support_type=msg.recommended_support_type,
            matched_peers=matched_peers,
            group_sessions=relevant_groups,
            activation_reason=f"Activated for: {', '.join(msg.patterns)}"
        )
        
        await ctx.send(SORO_ORCHESTRATOR_ADDRESS, activation)
        print(f"✅ PSN: ACTIVATION SENT to Orchestrator")
        print(f"   👥 Matched {len(matched_peers)} peers")
        for peer in matched_peers:
            print(f"      • {peer['name']} - {peer['match_reason']}")
            
        print(f"   📅 Found {len(relevant_groups)} groups") 
        for group in relevant_groups:
            print(f"      • {group['topic']} - {group['schedule']}")
            
    except Exception as e:
        print(f"❌ PSN: Processing failed - {e}")

psn_connect.include(peer_match_proto, publish_manifest=True)

if __name__ == "__main__":
    print("🚀 Starting PSN Connect...")
    psn_connect.run()