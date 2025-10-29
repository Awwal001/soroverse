#!/usr/bin/env python3
"""
SoroMind Core Agent - Fixed with proper path and .env setup
"""

import os
import sys
from pathlib import Path

# Add project root to Python path - CRITICAL FIX
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load .env file - CRITICAL FIX
from dotenv import load_dotenv
load_dotenv()

# Verify environment variables
required_vars = ['ASI_API_KEY', 'AGENTVERSE_API_KEY', 'SOROMIND_SEED']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print(f"❌ Missing environment variables: {missing_vars}")
    print("💡 Make sure .env file exists and contains all required variables")
    print("💡 Current .env location should be: /Users/mac/Desktop/soroverse/.env")
    sys.exit(1)

print("✅ Environment variables loaded successfully")

# Now import the rest
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4

from uagents import Agent, Context, Protocol, Model
from uagents_core.contrib.protocols.chat import (
    ChatMessage, ChatAcknowledgement, TextContent,
    StartSessionContent, EndSessionContent, chat_protocol_spec
)

from models.data_models import (
    MentalSupportRequest, SupportResponse, RiskLevel, 
    ResponseType, SupportType, MentalStateAlert
)
from knowledge.metta_manager import MeTTaManager
from utils.asi_client import ASIClient
from utils.crisis_detector import CrisisDetector

# Rest of your code continues...


# Initialize core components
metta_manager = MeTTaManager()
asi_client = ASIClient()
crisis_detector = CrisisDetector()

class UserSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.now(timezone.utc)
        self.message_history: List[Dict] = []
        self.user_patterns: List[str] = []
        self.risk_level = RiskLevel.LOW
        self.intervention_history: List[str] = []

    def add_message(self, role: str, content: str):
        self.message_history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now(timezone.utc)
        })
        
        # Keep only last 20 messages
        if len(self.message_history) > 20:
            self.message_history = self.message_history[-20:]

# Initialize SoroMind Core Agent
soromind = Agent(
    name="SoroMind Core",
    seed=os.getenv("SOROMIND_SEED", "soromind_core_secret_phrase_001"),
    endpoint=["https://couponless-dottie-uninstrumental.ngrok-free.dev/submit"],
    mailbox=True
)

# Active user sessions
user_sessions: Dict[str, UserSession] = {}

# Chat Protocol for ASI:One compatibility
chat_proto = Protocol(spec=chat_protocol_spec)

@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages from ASI:One or other agents"""
    ctx.logger.info(f"Received chat message from {sender}")
    
    # Send acknowledgement
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.now(timezone.utc),
            acknowledged_msg_id=msg.msg_id
        )
    )

    # Process message content
    user_message = ""
    session_id = None
    
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"New chat session started with {sender}")
            session_id = str(uuid4())
            user_sessions[session_id] = UserSession(session_id)
            continue
            
        elif isinstance(item, TextContent):
            user_message = item.text
            ctx.logger.info(f"Processing user message: {user_message}")
            
            # Get or create session
            if not session_id:
                session_id = str(uuid4())
                user_sessions[session_id] = UserSession(session_id)
            
            session = user_sessions[session_id]
            session.add_message("user", user_message)
            
            # Process the message
            response = await process_user_message(ctx, user_message, session)
            
            # Send response back
            response_msg = ChatMessage(
                timestamp=datetime.now(timezone.utc),
                msg_id=uuid4(),
                content=[TextContent(type="text", text=response)]
            )
            
            await ctx.send(sender, response_msg)
            
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"Chat session ended with {sender}")
            if session_id and session_id in user_sessions:
                del user_sessions[session_id]

@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle message acknowledgements"""
    ctx.logger.info(f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}")

async def process_user_message(ctx: Context, message: str, session: UserSession) -> str:
    """Process user message and generate appropriate response"""
    try:
        # 1. Crisis detection
        crisis_assessment = crisis_detector.detect_crisis_indicators(message)
        session.risk_level = crisis_assessment['risk_level']
        
        if crisis_assessment['immediate_action_required']:
            crisis_response = crisis_detector.get_crisis_response(crisis_assessment)
            await trigger_crisis_alert(ctx, session, crisis_assessment)
            return format_crisis_response(crisis_response)
        
        # 2. Pattern analysis using ASI:One
        analysis = await asi_client.analyze_mental_patterns(
            message, 
            [msg['content'] for msg in session.message_history if msg['role'] == 'user']
        )
        
        # Update session patterns
        session.user_patterns.extend(analysis.patterns)
        session.user_patterns = list(set(session.user_patterns))  # Remove duplicates
        
        # 3. Get interventions from MeTTa knowledge graph
        interventions = []
        for pattern in analysis.patterns[:3]:  # Limit to top 3 patterns
            pattern_interventions = metta_manager.get_interventions_for_pattern(pattern)
            interventions.extend(pattern_interventions)
        
        # 4. Generate empathetic response
        response = generate_empathetic_response(
            message, analysis, interventions, session
        )
        
        session.add_message("assistant", response)
        return response
        
    except Exception as e:
        ctx.logger.error(f"Error processing user message: {e}")
        return "I apologize, but I'm having trouble processing your message right now. Please try again or reach out to a mental health professional if you need immediate support."

async def trigger_crisis_alert(ctx: Context, session: UserSession, crisis_assessment: Dict):
    """Trigger crisis alert to other agents"""
    alert = MentalStateAlert(
        user_id=session.session_id,
        risk_level=session.risk_level,
        detected_patterns=session.user_patterns,
        recommended_actions=crisis_assessment.get('actions', []),
        timestamp=datetime.now(timezone.utc)
    )
    
    # In a full implementation, this would send to SOMA Engine and Crisis Monitor
    ctx.logger.warning(f"CRISIS ALERT: User {session.session_id} - Level: {session.risk_level}")

def generate_empathetic_response(
    user_message: str, 
    analysis, 
    interventions: List[Dict], 
    session: UserSession
) -> str:
    """Generate an empathetic and helpful response"""
    
    # Start with validation and empathy
    response_parts = [
        "I hear you, and I appreciate you sharing what you're going through.",
        "It sounds like you're dealing with some challenging thoughts and feelings."
    ]
    
    # Add pattern insights if available
    if analysis.patterns:
        patterns_text = ", ".join(analysis.patterns[:2])
        response_parts.append(f"I notice some patterns of {patterns_text} in what you're describing.")
    
    # Add intervention suggestions
    if interventions:
        top_intervention = interventions[0]
        response_parts.append(
            f"Based on what you're experiencing, you might find {top_intervention['name']} helpful. "
            f"This approach has shown good effectiveness for similar situations."
        )
        
        # Add brief instructions if available
        if 'details' in top_intervention and 'technique' in top_intervention['details']:
            response_parts.append(f"Technique: {top_intervention['details']['technique']}")
    
    # Add peer support suggestion for medium risk
    if session.risk_level == RiskLevel.MEDIUM:
        response_parts.append(
            "Would you be interested in connecting with others who have similar experiences? "
            "Peer support can be really valuable."
        )
    
    # End with open question
    response_parts.append(
        "How does that sound to you? Would you like to explore any of these approaches further, "
        "or is there something specific you'd like to focus on?"
    )
    
    return " ".join(response_parts)

def format_crisis_response(crisis_response: Dict) -> str:
    """Format crisis response with appropriate urgency and resources"""
    response_lines = [crisis_response['message']]
    response_lines.append("\nImmediate resources:")
    
    for action in crisis_response['actions']:
        response_lines.append(f"• {action}")
    
    response_lines.append(
        "\nPlease reach out for help. You don't have to go through this alone. "
        "Professional support is available and can make a real difference."
    )
    
    return "\n".join(response_lines)

# Include the chat protocol
soromind.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    print("🚀 Starting SoroMind Core Agent...")
    print(f"📍 Agent address: {soromind.address}")
    print("🔗 Chat Protocol enabled for ASI:One compatibility")
    soromind.run()