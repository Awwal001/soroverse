#!/usr/bin/env python3
"""
PSN Connect Agent - Peer Support Network with Custom Chat Protocol
Fixed for uagents compatibility
"""

import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

import random
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from enum import Enum

from uagents import Agent, Context, Protocol, Model

# Custom Models for PSN Connect (Fixed for uagents compatibility)
class PSNChatMessage(Model):
    """Custom chat message model for PSN Connect"""
    message_id: str
    sender_id: str
    recipient_id: str
    content: str
    message_type: str = "text"
    timestamp: str
    session_id: Optional[str] = None

class PSNChatResponse(Model):
    """Response model for PSN chat messages"""
    response_id: str
    original_message_id: str
    content: str
    responder_id: str
    response_type: str = "support"
    timestamp: str

class SupportRequestType(str, Enum):
    IMMEDIATE = "immediate"
    SCHEDULED = "scheduled"
    GROUP = "group"

class PeerSupportRequest(Model):
    """Request for peer support matching"""
    request_id: str
    user_id: str
    current_state: str
    support_type: SupportRequestType
    availability: List[str]
    expertise_areas: List[str]
    urgency_level: str = "medium"
    preferences: Dict[str, Any] = {}

class PeerMatchResponse(Model):
    """Response with matched peers"""
    matched_peers: List[Dict[str, Any]]
    match_confidence: float
    group_sessions: List[Dict[str, Any]]
    recommended_approach: str
    estimated_wait_time: int

class SupportSession(Model):
    """Ongoing support session model"""
    session_id: str
    user_id: str
    peer_id: str
    start_time: str
    status: str = "active"
    messages: List[Dict[str, str]] = []

# PSN Connect Agent
psn_connect = Agent(
    name="PSN Connect",
    seed=os.getenv("PSN_CONNECT_SEED", "psn_connect_secret_phrase_004"),
    port=8003,
    endpoint=["http://localhost:8003/submit"],
    mailbox=True
)

# Mock databases
PEER_SUPPORTERS = [
    {
        'id': 'peer_001',
        'name': 'Alex',
        'expertise': ['academic_stress', 'anxiety', 'time_management'],
        'availability': ['evening', 'weekend'],
        'languages': ['English'],
        'experience_level': 'experienced',
        'rating': 4.8,
        'support_style': 'structured',
        'specialties': ['college_students', 'young_adults']
    },
    {
        'id': 'peer_002', 
        'name': 'Taylor',
        'expertise': ['work_anxiety', 'imposter_syndrome', 'career_transition'],
        'availability': ['weekday', 'lunch', 'evening'],
        'languages': ['English', 'Spanish'],
        'experience_level': 'trained',
        'rating': 4.6,
        'support_style': 'conversational',
        'specialties': ['professionals', 'career_changers']
    },
    {
        'id': 'peer_003',
        'name': 'Jordan',
        'expertise': ['relationship_issues', 'loneliness', 'social_anxiety'],
        'availability': ['flexible'],
        'languages': ['English'],
        'experience_level': 'peer',
        'rating': 4.7,
        'support_style': 'empathetic',
        'specialties': ['young_adults', 'social_support']
    },
    {
        'id': 'peer_004',
        'name': 'Casey',
        'expertise': ['grief_loss', 'life_transitions', 'family_issues'],
        'availability': ['weekend', 'evening'],
        'languages': ['English'],
        'experience_level': 'experienced',
        'rating': 4.9,
        'support_style': 'validating',
        'specialties': ['adults', 'life_transitions']
    },
    {
        'id': 'peer_005',
        'name': 'Riley',
        'expertise': ['mindfulness', 'stress_management', 'self_care'],
        'availability': ['morning', 'lunch'],
        'languages': ['English', 'French'],
        'experience_level': 'trained',
        'rating': 4.5,
        'support_style': 'mindfulness_based',
        'specialties': ['stress_management', 'wellness']
    }
]

GROUP_SESSIONS = [
    {
        'id': 'group_001',
        'topic': 'Academic Stress Management',
        'schedule': 'Weekly on Mondays 6 PM',
        'facilitator': 'Dr. Maria Chen',
        'size': '8-12 participants',
        'focus': 'Study techniques, time management, stress reduction',
        'format': 'virtual',
        'duration': '60 minutes'
    },
    {
        'id': 'group_002',
        'topic': 'Anxiety Support Circle',
        'schedule': 'Twice weekly - Tues/Thurs 7 PM', 
        'facilitator': 'James Wilson',
        'size': '6-10 participants',
        'focus': 'Coping strategies, mindfulness, peer sharing',
        'format': 'virtual',
        'duration': '90 minutes'
    },
    {
        'id': 'group_003',
        'topic': 'Work-Life Balance',
        'schedule': 'Weekly on Wednesdays 12 PM',
        'facilitator': 'Sarah Johnson',
        'size': '10-15 participants',
        'focus': 'Boundary setting, stress management, career growth',
        'format': 'in_person',
        'duration': '75 minutes'
    },
    {
        'id': 'group_004',
        'topic': 'Mindfulness and Meditation',
        'schedule': 'Daily 8 AM',
        'facilitator': 'Riley Smith',
        'size': 'Unlimited',
        'focus': 'Guided meditation, breathing exercises',
        'format': 'virtual',
        'duration': '30 minutes'
    }
]

# Active support sessions
active_sessions: Dict[str, Dict] = {}

# Helper functions for default values
def generate_message_id():
    return str(uuid.uuid4())

def generate_timestamp():
    return datetime.now(timezone.utc).isoformat()

# Custom Chat Protocol for PSN
psn_chat_proto = Protocol(name="PSNChat", version="1.0.0")

@psn_chat_proto.on_message(PSNChatMessage)
async def handle_psn_chat(ctx: Context, sender: str, msg: PSNChatMessage):
    """Handle PSN-specific chat messages between users and peers"""
    ctx.logger.info(f"📨 PSN Chat received from {msg.sender_id} to {msg.recipient_id}")
    
    try:
        # Log the message
        print(f"💬 PSN Chat: {msg.sender_id} -> {msg.recipient_id}: {msg.content}")
        
        # Store message in session if applicable
        if msg.session_id and msg.session_id in active_sessions:
            session = active_sessions[msg.session_id]
            session['messages'].append({
                'sender': msg.sender_id,
                'content': msg.content,
                'timestamp': msg.timestamp
            })
        
        # Generate appropriate response based on message type
        if msg.message_type == "support_request":
            response_content = generate_support_response(msg.content)
            response_type = "support"
        elif msg.message_type == "encouragement":
            response_content = generate_encouragement_response(msg.content)
            response_type = "encouragement"
        else:
            response_content = generate_general_response(msg.content)
            response_type = "general"
        
        # Create and send response
        response = PSNChatResponse(
            response_id=generate_message_id(),
            original_message_id=msg.message_id,
            content=response_content,
            responder_id=msg.recipient_id,
            response_type=response_type,
            timestamp=generate_timestamp()
        )
        
        await ctx.send(sender, response)
        ctx.logger.info(f"✅ PSN Chat response sent to {msg.sender_id}")
        
    except Exception as e:
        ctx.logger.error(f"❌ PSN Chat error: {e}")
        # Send error response
        error_response = PSNChatResponse(
            response_id=generate_message_id(),
            original_message_id=msg.message_id,
            content="I apologize, but I'm having trouble processing your message right now. Please try again.",
            responder_id="psn_system",
            response_type="error",
            timestamp=generate_timestamp()
        )
        await ctx.send(sender, error_response)

@psn_chat_proto.on_message(PSNChatResponse)
async def handle_psn_chat_response(ctx: Context, sender: str, msg: PSNChatResponse):
    """Handle responses to PSN chat messages"""
    ctx.logger.info(f"📩 PSN Chat response received from {msg.responder_id}")
    print(f"💬 PSN Response: {msg.responder_id}: {msg.content}")

# Peer Matching Protocol
peer_match_proto = Protocol(name="PeerSupportMatching", version="1.0.0")

@peer_match_proto.on_message(PeerSupportRequest)
async def handle_peer_match_request(ctx: Context, sender: str, msg: PeerSupportRequest):
    """Handle peer support matching requests"""
    ctx.logger.info(f"🔍 Peer match request for user {msg.user_id}")
    print(f"🎯 Matching peers for: {msg.current_state}")
    
    try:
        # Find matching peers
        matched_peers = find_matching_peers(
            msg.current_state,
            msg.support_type,
            msg.availability,
            msg.expertise_areas,
            msg.urgency_level
        )
        
        # Find relevant group sessions
        relevant_groups = find_relevant_groups(msg.current_state, msg.expertise_areas)
        
        # Calculate estimated wait time based on urgency
        wait_time = calculate_wait_time(msg.urgency_level, len(matched_peers))
        
        # Determine recommended approach
        recommended_approach = recommend_approach(msg.support_type, matched_peers, relevant_groups)
        
        response = PeerMatchResponse(
            matched_peers=matched_peers,
            match_confidence=calculate_match_confidence(matched_peers),
            group_sessions=relevant_groups,
            recommended_approach=recommended_approach,
            estimated_wait_time=wait_time
        )
        
        await ctx.send(sender, response)
        ctx.logger.info(f"✅ Sent peer match with {len(matched_peers)} matches")
        print(f"✅ Peer matching complete: {len(matched_peers)} matches found")
        
    except Exception as e:
        ctx.logger.error(f"❌ Peer matching error: {e}")
        error_response = PeerMatchResponse(
            matched_peers=[],
            match_confidence=0.0,
            group_sessions=[],
            recommended_approach="Unable to match at this time",
            estimated_wait_time=0
        )
        await ctx.send(sender, error_response)

@peer_match_proto.on_message(model=SupportSession)
async def handle_support_session(ctx: Context, sender: str, msg: SupportSession):
    """Handle support session management"""
    ctx.logger.info(f"🔄 Support session {msg.session_id} - Status: {msg.status}")
    
    if msg.status == "active":
        active_sessions[msg.session_id] = {
            'session_id': msg.session_id,
            'user_id': msg.user_id,
            'peer_id': msg.peer_id,
            'start_time': msg.start_time,
            'status': msg.status,
            'messages': msg.messages
        }
        print(f"🟢 Session started: {msg.session_id}")
    elif msg.status in ["completed", "cancelled"]:
        active_sessions.pop(msg.session_id, None)
        print(f"🔴 Session ended: {msg.session_id}")

# Support Functions
def find_matching_peers(
    current_state: str,
    support_type: SupportRequestType,
    availability: List[str],
    expertise_areas: List[str],
    urgency_level: str
) -> List[Dict[str, Any]]:
    """Find peers that match the user's needs and preferences"""
    
    matching_peers = []
    
    for peer in PEER_SUPPORTERS:
        match_score = calculate_peer_match_score(
            peer, current_state, support_type, availability, expertise_areas, urgency_level
        )
        
        if match_score > 0.3:  # Minimum match threshold
            peer_copy = peer.copy()
            peer_copy['match_score'] = round(match_score, 2)
            peer_copy['match_reason'] = get_match_reason(peer, expertise_areas)
            peer_copy['response_time'] = estimate_response_time(peer, urgency_level)
            matching_peers.append(peer_copy)
    
    # Sort by match score and return top matches
    matching_peers.sort(key=lambda x: x['match_score'], reverse=True)
    return matching_peers[:3]

def calculate_peer_match_score(
    peer: Dict[str, Any],
    current_state: str,
    support_type: SupportRequestType,
    availability: List[str],
    expertise_areas: List[str],
    urgency_level: str
) -> float:
    """Calculate how well a peer matches the user's needs"""
    score = 0.0
    
    # Expertise matching (40% weight)
    expertise_match = len(set(expertise_areas) & set(peer['expertise'])) / max(len(expertise_areas), 1)
    score += expertise_match * 0.4
    
    # Availability matching (25% weight)
    availability_match = len(set(availability) & set(peer['availability'])) / max(len(availability), 1)
    score += availability_match * 0.25
    
    # Experience level (20% weight)
    exp_weights = {'experienced': 1.0, 'trained': 0.8, 'peer': 0.6}
    score += exp_weights.get(peer['experience_level'], 0.5) * 0.2
    
    # Urgency compatibility (15% weight)
    if urgency_level == "high" and peer['experience_level'] in ['experienced', 'trained']:
        score += 0.15
    
    return min(score, 1.0)

def find_relevant_groups(current_state: str, expertise_areas: List[str]) -> List[Dict[str, Any]]:
    """Find relevant group sessions based on user's state and needs"""
    relevant_groups = []
    
    for group in GROUP_SESSIONS:
        group_text = f"{group['topic']} {group['focus']}".lower()
        user_keywords = current_state.lower().split() + [area.lower() for area in expertise_areas]
        
        # Count matching keywords
        keyword_matches = sum(1 for keyword in user_keywords if len(keyword) > 3 and keyword in group_text)
        
        if keyword_matches >= 1:  # At least one meaningful match
            group_copy = group.copy()
            group_copy['relevance_score'] = keyword_matches
            relevant_groups.append(group_copy)
    
    relevant_groups.sort(key=lambda x: x['relevance_score'], reverse=True)
    return relevant_groups[:2]

def calculate_match_confidence(matched_peers: List[Dict]) -> float:
    """Calculate overall confidence in peer matches"""
    if not matched_peers:
        return 0.0
    
    avg_match_score = sum(peer['match_score'] for peer in matched_peers) / len(matched_peers)
    return round(avg_match_score, 2)

def calculate_wait_time(urgency_level: str, available_peers: int) -> int:
    """Calculate estimated wait time in minutes"""
    base_times = {"low": 120, "medium": 45, "high": 15}
    peer_modifier = max(0, 3 - available_peers) * 10  # Longer wait if fewer peers
    return base_times.get(urgency_level, 60) + peer_modifier

def recommend_approach(support_type: SupportRequestType, peers: List, groups: List) -> str:
    """Recommend the best support approach"""
    if support_type == SupportRequestType.IMMEDIATE and peers:
        return "One-on-one peer support recommended for immediate needs"
    elif support_type == SupportRequestType.GROUP and groups:
        return "Group session recommended for shared experiences"
    elif peers and groups:
        return "Combination of peer support and group sessions recommended"
    elif peers:
        return "One-on-one peer support recommended"
    elif groups:
        return "Group sessions recommended"
    else:
        return "Self-guided resources recommended while matching"

def estimate_response_time(peer: Dict, urgency: str) -> str:
    """Estimate how quickly a peer typically responds"""
    base_times = {"experienced": 15, "trained": 30, "peer": 45}
    base_time = base_times.get(peer['experience_level'], 30)
    
    if urgency == "high":
        return f"{max(5, base_time // 2)}-{base_time} minutes"
    else:
        return f"{base_time}-{base_time * 2} minutes"

def get_match_reason(peer: Dict, expertise_areas: List[str]) -> str:
    """Generate reason for match"""
    matching_expertise = [area for area in expertise_areas if area in peer['expertise']]
    
    if matching_expertise:
        return f"Expertise in {', '.join(matching_expertise[:2])}"
    elif peer['support_style']:
        return f"{peer['support_style'].title()} support style"
    else:
        return "General peer support availability"

def generate_support_response(content: str) -> str:
    """Generate supportive response for support requests"""
    support_responses = [
        "I hear you're going through a tough time. You're not alone in this.",
        "It takes courage to reach out for support. I'm here to listen.",
        "Thank you for sharing what you're experiencing. Let's work through this together.",
        "I understand this is challenging. What would be most helpful for you right now?",
        "You've taken an important step by reaching out. Let's explore how I can support you."
    ]
    return random.choice(support_responses)

def generate_encouragement_response(content: str) -> str:
    """Generate encouraging responses"""
    encouragement_responses = [
        "You're doing better than you think. Keep going!",
        "Progress isn't always linear - every small step counts.",
        "Remember how far you've come, not just how far you have to go.",
        "You have strengths you might not even recognize yet.",
        "Be kind to yourself today. You're doing the best you can."
    ]
    return random.choice(encouragement_responses)

def generate_general_response(content: str) -> str:
    """Generate general chat responses"""
    general_responses = [
        "I'm here to support you. How can I help today?",
        "Thank you for reaching out. What's on your mind?",
        "I'm listening. Tell me more about what you're experiencing.",
        "Let's work together to find the support you need.",
        "I'm here to help you navigate this. What would you like to focus on?"
    ]
    return random.choice(general_responses)

# Include both protocols
psn_connect.include(psn_chat_proto, publish_manifest=True)
psn_connect.include(peer_match_proto, publish_manifest=True)

if __name__ == "__main__":
    print("=" * 50)
    print("🤝 PSN CONNECT - PEER SUPPORT NETWORK")
    print("=" * 50)
    print(f"📍 Agent Address: {psn_connect.address}")
    print(f"🌐 Local URL: http://localhost:8003/submit")
    print("💬 Custom PSN Chat Protocol enabled")
    print("👥 Peer support matching and community coordination ready")
    print("=" * 50)
    
    try:
        psn_connect.run()
    except KeyboardInterrupt:
        print("\n🛑 PSN Connect agent stopped")
    except Exception as e:
        print(f"❌ Error: {e}")