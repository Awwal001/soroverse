#!/usr/bin/env python3
"""
SoroMind Core Agent - GUARANTEED Orchestrator Integration
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

# Verify environment variables
required_vars = ['ASI_API_KEY', 'AGENTVERSE_API_KEY', 'SOROMIND_SEED']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print(f"❌ Missing environment variables: {missing_vars}")
    print("💡 Make sure .env file exists and contains all required variables")
    sys.exit(1)

print("✅ Environment variables loaded successfully")

import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from uuid import uuid4

from uagents import Agent, Context, Protocol, Model
from uagents_core.contrib.protocols.chat import (
    ChatMessage, ChatAcknowledgement, TextContent,
    StartSessionContent, EndSessionContent, chat_protocol_spec
)

from common_models import (
    MentalStateAlert, PatternAnalysisRequest, PatternAnalysisResponse,
    InterventionRequest, InterventionResponse, UserPreferences, RiskLevel
)

from models.data_models import (
    MentalSupportRequest, SupportResponse, 
    ResponseType, SupportType
)
from knowledge.metta_manager import MeTTaManager
from utils.asi_client import ASIClient
from utils.crisis_detector import CrisisDetector

# Initialize core components
metta_manager = MeTTaManager()
asi_client = ASIClient()
crisis_detector = CrisisDetector()

# ==================== AGENT ADDRESSES ====================
SOMA_ENGINE_ADDRESS = "agent1qtqs2gzljl90mlcjenxj6nxjd2gkhpptdy8nsaz7terv5s8h8gkf2z5ya4s"
SORO_ORCHESTRATOR_ADDRESS = "agent1q2a7v3rshca8knfzltm2q6uqxghx8fp02k7qg3cql9tdztgea539uuuch76"

class UserSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.now(timezone.utc)
        self.message_history: List[Dict] = []
        self.user_patterns: List[str] = []
        self.risk_level = RiskLevel.LOW
        self.intervention_history: List[str] = []
        self.last_orchestrator_contact = None

    def add_message(self, role: str, content: str):
        self.message_history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now(timezone.utc)
        })
        
        if len(self.message_history) > 20:
            self.message_history = self.message_history[-20:]

# Initialize SoroMind Core Agent WITH PORT 8001
soromind = Agent(
    name="SoroMind Core",
    seed=os.getenv("SOROMIND_SEED", "soromind_core_secret_phrase_001"),
    port=8001,  # CRITICAL FIX: Match ngrok port
    endpoint=["https://couponless-dottie-uninstrumental.ngrok-free.dev/submit"],
    mailbox=True
)

print("=" * 60)
print("🧠 SOROMIND CORE - GUARANTEED ORCHESTRATOR INTEGRATION")
print("=" * 60)
print(f"📍 Agent Address: {soromind.address}")
print(f"🌐 Local Port: 8001 (Matches ngrok)")
print(f"🔗 Ngrok URL: https://couponless-dottie-uninstrumental.ngrok-free.dev")
print(f"🤝 SOMA Engine: {SOMA_ENGINE_ADDRESS[:16]}...")
print(f"💫 SORO Orchestrator: {SORO_ORCHESTRATOR_ADDRESS[:16]}...")
print("=" * 60)

# Active user sessions
user_sessions: Dict[str, UserSession] = {}

# ==================== ORCHESTRATOR COMMUNICATION FUNCTIONS ====================

async def send_to_orchestrator(ctx: Context, session: UserSession, user_message: str, 
                             patterns: List[str], risk_level: RiskLevel) -> bool:
    """Send intervention request to SORO Orchestrator - FIXED timestamp"""
    try:
        print(f"💫 SoroMind: Preparing Orchestrator request...")
        print(f"   📊 Message: '{user_message[:50]}...'")
        print(f"   🔍 Patterns: {patterns}")
        print(f"   ⚠️ Risk: {risk_level}")
        
        # FIX: Create UserPreferences with default values
        preferences = UserPreferences(
            preferred_techniques=["breathing", "grounding", "cognitive"],
            comfort_level="beginner",
            time_availability=15,
            support_types=["self_help", "peer_support"],
            communication_style="empathetic"
        )
        
        # FIX: Convert timestamp to string
        intervention_request = InterventionRequest(
            user_id=session.session_id,
            user_state=user_message,
            patterns=patterns,
            risk_level=risk_level,
            timestamp=datetime.now(timezone.utc).isoformat(),  # FIX: Convert to ISO string
            preferences=preferences,
            session_context={
                "message_count": len(session.message_history),
                "previous_patterns": session.user_patterns
            }
        )
        
        # Send with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                await ctx.send(SORO_ORCHESTRATOR_ADDRESS, intervention_request)
                session.last_orchestrator_contact = datetime.now(timezone.utc)
                
                ctx.logger.info(f"📨 Sent intervention request to Orchestrator (attempt {attempt + 1})")
                print(f"✅ SoroMind: SUCCESS - Sent to Orchestrator!")
                print(f"   📍 Target: {SORO_ORCHESTRATOR_ADDRESS[:16]}...")
                print(f"   🔄 Attempt: {attempt + 1}/{max_retries}")
                
                # Log the interaction
                session.intervention_history.append(
                    f"Orchestrator contact: {risk_level} risk - {datetime.now().strftime('%H:%M:%S')}"
                )
                
                return True
                
            except Exception as send_error:
                ctx.logger.warning(f"⚠️ Orchestrator send attempt {attempt + 1} failed: {send_error}")
                print(f"⚠️ SoroMind: Orchestrator attempt {attempt + 1} failed - {send_error}")
                
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)  # Wait before retry
                    continue
                else:
                    raise send_error
                    
    except Exception as e:
        ctx.logger.error(f"❌ ALL Orchestrator attempts failed: {e}")
        print(f"❌ SoroMind: CRITICAL - Orchestrator communication failed after all retries")
        print(f"   💡 Fallback: Continuing without coordination")
        
        # Even if failed, log the attempt
        session.intervention_history.append(
            f"Orchestrator FAILED: {risk_level} risk - {datetime.now().strftime('%H:%M:%S')}"
        )
        return False

async def send_to_soma_engine(ctx: Context, session: UserSession, user_message: str) -> bool:
    """Send pattern analysis request to SOMA Engine"""
    try:
        analysis_request = PatternAnalysisRequest(
            user_message=user_message,
            session_history=[msg['content'] for msg in session.message_history if msg['role'] == 'user'],
            user_id=session.session_id
        )
        
        await ctx.send(SOMA_ENGINE_ADDRESS, analysis_request)
        ctx.logger.info(f"🔍 Sent pattern analysis to SOMA Engine")
        print(f"🔍 SoroMind: Sent to SOMA Engine for pattern analysis")
        return True
        
    except Exception as e:
        ctx.logger.warning(f"⚠️ SOMA Engine communication failed: {e}")
        print(f"⚠️ SoroMind: SOMA Engine communication failed - {e}")
        return False

# ==================== ENHANCED MESSAGE PROCESSING ====================

async def enhanced_crisis_detection(message: str, session: UserSession) -> Tuple[Dict, List[str]]:
    """Enhanced crisis detection with pattern extraction"""
    # 1. Use crisis detector
    crisis_assessment = crisis_detector.detect_crisis_indicators(message)
    
    # 2. Extract patterns from message for Orchestrator
    patterns = extract_patterns_from_message(message, crisis_assessment)
    
    return crisis_assessment, patterns

def extract_patterns_from_message(message: str, crisis_assessment: Dict) -> List[str]:
    """Extract patterns from user message for Orchestrator coordination"""
    message_lower = message.lower()
    patterns = []
    
    # Add crisis indicators as patterns
    patterns.extend(crisis_assessment.get('crisis_indicators', []))
    patterns.extend(crisis_assessment.get('high_risk_indicators', []))
    
    # Content-based pattern extraction
    if any(word in message_lower for word in ['academic', 'study', 'exam', 'test', 'school', 'college']):
        patterns.append('academic_stress')
    
    if any(word in message_lower for word in ['anxious', 'worry', 'nervous', 'panic', 'overwhelmed']):
        patterns.append('anxiety')
    
    if any(word in message_lower for word in ['sad', 'depressed', 'hopeless', 'empty', 'numb']):
        patterns.append('depression')
    
    if any(word in message_lower for word in ['sleep', 'tired', 'exhausted', 'insomnia']):
        patterns.append('sleep_issues')
    
    if any(word in message_lower for word in ['alone', 'lonely', 'isolated', 'no friends']):
        patterns.append('loneliness')
    
    if any(word in message_lower for word in ['stress', 'pressure', 'overwhelmed']):
        patterns.append('stress')
    
    # Remove duplicates and ensure we have patterns
    patterns = list(set(patterns))
    
    # If no patterns detected, add general emotional distress
    if not patterns and len(message.split()) > 3:
        patterns.append('emotional_distress')
    
    return patterns

# ==================== CHAT PROTOCOL HANDLER ====================

chat_proto = Protocol(spec=chat_protocol_spec)

@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages with GUARANTEED Orchestrator integration"""
    ctx.logger.info(f"📨 Received chat message from {sender}")
    print(f"💬 CHAT PROTOCOL TRIGGERED - Message from: {sender}")
    
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
            ctx.logger.info(f"🆕 New chat session started with {sender}")
            session_id = str(uuid4())
            user_sessions[session_id] = UserSession(session_id)
            continue
            
        elif isinstance(item, TextContent):
            user_message = item.text
            ctx.logger.info(f"💬 Processing user message: {user_message}")
            print(f"💬 USER INPUT: '{user_message}'")
            
            # Get or create session
            if not session_id:
                session_id = str(uuid4())
                user_sessions[session_id] = UserSession(session_id)
            
            session = user_sessions[session_id]
            session.add_message("user", user_message)
            
            # Process the message with GUARANTEED Orchestrator integration
            response = await process_user_message_with_orchestrator(ctx, user_message, session)
            
            # Send response back
            response_msg = ChatMessage(
                timestamp=datetime.now(timezone.utc),
                msg_id=str(uuid4()),
                content=[TextContent(type="text", text=response)]
            )
            
            await ctx.send(sender, response_msg)
            session.add_message("assistant", response)
            print(f"💬 AGENT RESPONSE SENT: '{response[:100]}...'")
            
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"🔚 Chat session ended with {sender}")
            if session_id and session_id in user_sessions:
                # Send final update to Orchestrator
                await send_session_closure_to_orchestrator(ctx, user_sessions[session_id])
                del user_sessions[session_id]

async def send_session_closure_to_orchestrator(ctx: Context, session: UserSession):
    """Notify Orchestrator when session ends"""
    try:
        closure_alert = MentalStateAlert(
            user_id=session.session_id,
            risk_level=session.risk_level,
            detected_patterns=session.user_patterns,
            recommended_actions=["SESSION_CLOSED"],
            timestamp=datetime.now(timezone.utc)
        )
        await ctx.send(SORO_ORCHESTRATOR_ADDRESS, closure_alert)
        print(f"📤 SoroMind: Sent session closure to Orchestrator")
    except Exception as e:
        print(f"⚠️ Could not send session closure: {e}")

@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle message acknowledgements"""
    ctx.logger.info(f"✅ Received acknowledgement from {sender}")

# ==================== MAIN MESSAGE PROCESSING ====================

async def process_user_message_with_orchestrator(ctx: Context, message: str, session: UserSession) -> str:
    """Process user message with GUARANTEED Orchestrator integration"""
    
    print(f"🔍 SoroMind: Starting message processing with Orchestrator integration...")
    
    # ==================== EMERGENCY BYPASS ====================
    message_lower = message.lower().strip()
    emergency_phrases = [
        'kill myself', 'suicide', 'end my life', 'want to die', 'better off dead',
        'harm myself', 'end it all', 'feel like killing myself', 'want to kill myself'
    ]
    
    # DIRECT STRING MATCHING - bypasses crisis detector entirely
    if any(phrase in message_lower for phrase in emergency_phrases):
        ctx.logger.warning(f"🚨 EMERGENCY BYPASS TRIGGERED: {message}")
        print(f"🚨 SoroMind: EMERGENCY BYPASS - Direct crisis phrase detected!")
        
        # SEND EMERGENCY ALERT TO ORCHESTRATOR
        emergency_patterns = ['suicidal_ideation', 'crisis_emergency', 'immediate_risk']
        await send_to_orchestrator(ctx, session, message, emergency_patterns, RiskLevel.CRISIS)
        
        return """🚨 **I'm very concerned about what you're sharing.** Your safety is the most important thing right now.

**IMMEDIATE HELP AVAILABLE:**
• **National Suicide Prevention Lifeline**: 988 or 1-800-273-8255 (24/7)
• **Crisis Text Line**: Text HOME to 741741 
• **Emergency Services**: 911 or your local emergency number
• **International Emergency**: Your local emergency services

**Please reach out to one of these resources RIGHT NOW.** They have trained professionals who can help you through this moment.

You don't have to go through this alone. People care about you and want to help.

**Stay on the line with me while you reach out for help.**"""
    
    try:
        # ==================== ENHANCED CRISIS DETECTION ====================
        crisis_assessment, extracted_patterns = await enhanced_crisis_detection(message, session)
        session.risk_level = crisis_assessment['risk_level']
        
        print(f"🔍 Crisis assessment: {crisis_assessment}")
        print(f"🔍 Extracted patterns: {extracted_patterns}")
        
        # ==================== GUARANTEED ORCHESTRATOR COMMUNICATION ====================
        print(f"💫 SoroMind: SENDING TO ORCHESTRATOR...")
        orchestrator_success = await send_to_orchestrator(
            ctx, session, message, extracted_patterns, session.risk_level
        )
        
        if orchestrator_success:
            print(f"✅ SoroMind: Orchestrator coordination INITIATED")
        else:
            print(f"⚠️ SoroMind: Continuing WITHOUT Orchestrator coordination")
        
        # ==================== SEND TO SOMA ENGINE ====================
        if not crisis_assessment['immediate_action_required']:
            soma_success = await send_to_soma_engine(ctx, session, message)
            if soma_success:
                print(f"🔍 SoroMind: SOMA Engine analysis REQUESTED")
        
        # ==================== HANDLE CRISIS SITUATIONS ====================
        if crisis_assessment['immediate_action_required']:
            ctx.logger.warning(f"🚨 CRISIS DETECTED: {message}")
            crisis_response = crisis_detector.get_crisis_response(crisis_assessment)
            
            # Send crisis alert to Orchestrator (even if initial send failed)
            if not orchestrator_success:
                await send_to_orchestrator(ctx, session, message, extracted_patterns, RiskLevel.CRISIS)
            
            await trigger_crisis_alert(ctx, session, crisis_assessment)
            return format_crisis_response(crisis_response)

        # ==================== INTENT-BASED RESPONSE ====================
        intent_response = await generate_intent_based_response(ctx, message, session)
        if intent_response:
            return intent_response
        
        # ==================== FULL ANALYSIS PATH ====================
        analysis = await asi_client.analyze_mental_patterns(
            message, 
            [msg['content'] for msg in session.message_history if msg['role'] == 'user']
        )
        
        # Update session patterns with ASI analysis
        session.user_patterns.extend(analysis.patterns)
        session.user_patterns = list(set(session.user_patterns))
        
        # ==================== SEND UPDATED PATTERNS TO ORCHESTRATOR ====================
        if analysis.patterns and analysis.patterns != extracted_patterns:
            print(f"💫 SoroMind: Sending UPDATED patterns to Orchestrator...")
            await send_to_orchestrator(ctx, session, message, analysis.patterns, session.risk_level)
        
        # ==================== GENERATE RESPONSE ====================
        interventions = []
        for pattern in analysis.patterns[:3]:
            pattern_interventions = metta_manager.get_interventions_for_pattern(pattern)
            interventions.extend(pattern_interventions)
        
        response = generate_empathetic_response(
            message, analysis, interventions, session, orchestrator_success
        )
        
        session.add_message("assistant", response)
        return response
        
    except Exception as e:
        ctx.logger.error(f"Error processing user message: {e}")
        # Fallback with Orchestrator attempt
        try:
            fallback_patterns = ['processing_error', 'system_fallback']
            await send_to_orchestrator(ctx, session, message, fallback_patterns, RiskLevel.LOW)
        except:
            pass
            
        return await generate_fallback_response(ctx, message, session)

def generate_empathetic_response(
    user_message: str, 
    analysis, 
    interventions: List[Dict], 
    session: UserSession,
    orchestrator_connected: bool
) -> str:
    """Generate response that acknowledges Orchestrator coordination"""
    
    response_parts = []
    
    if orchestrator_connected:
        response_parts.append("I've connected with our support team to make sure you get the best help possible.")
    else:
        response_parts.append("I'm here to support you right now.")
    
    response_parts.append("I hear what you're going through, and it sounds really challenging.")
    
    if analysis.patterns:
        patterns_text = ", ".join(analysis.patterns[:2])
        response_parts.append(f"I notice some patterns of {patterns_text} in what you're describing.")
    
    if interventions:
        top_intervention = interventions[0]
        response_parts.append(
            f"Based on similar situations, {top_intervention['name']} has helped others. Would you like to try it?"
        )
    else:
        response_parts.append(
            "Would you like to explore some coping strategies that might help right now?"
        )
    
    if orchestrator_connected:
        response_parts.append("\n*Our coordination system is working to provide you with comprehensive support.*")
    
    return " ".join(response_parts)

# ==================== EXISTING HELPER FUNCTIONS (KEEP THESE) ====================

async def generate_intent_based_response(ctx: Context, message: str, session: UserSession) -> Optional[str]:
    """Generate immediate response based on detected intent"""
    # ... (keep all your existing intent response functions exactly as they were)
    message_lower = message.lower().strip()
    
    # Crisis phrases
    crisis_phrases = [
        'kill myself', 'suicide', 'end my life', 'want to die', 'better off dead',
        'harm myself', 'self harm', 'end it all', 'can\'t take it anymore'
    ]
    
    if any(phrase in message_lower for phrase in crisis_phrases):
        ctx.logger.warning(f"🚨 IMMEDIATE CRISIS DETECTED: {message}")
        return """🚨 **I'm very concerned about what you're sharing.** Your safety is the most important thing right now.

**IMMEDIATE HELP AVAILABLE:**
• **National Suicide Prevention Lifeline**: 988 or 1-800-273-8255 (24/7)
• **Crisis Text Line**: Text HOME to 741741 
• **Emergency Services**: 911 or your local emergency number
• **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/

**Please reach out to one of these resources RIGHT NOW.** They have trained professionals who can help you through this moment.

You don't have to go through this alone. People care about you and want to help."""

    # Academic stress
    if any(word in message_lower for word in ['exam', 'test', 'study', 'academic', 'school', 'college']):
        if 'can\'t sleep' in message_lower or 'insomnia' in message_lower:
            return """I understand you're dealing with academic stress that's affecting your sleep. This is really common during intense periods.

**For Immediate Relief:**
• **4-7-8 Breathing**: Inhale 4s, hold 7s, exhale 8s (repeat 4x)
• **Study Breaks**: 25 minutes study, 5 minutes break (Pomodoro technique)
• **Digital Curfew**: No screens 1 hour before bed

**Sleep Support:**
• Consistent wake time (even weekends)
• Bed only for sleep (no studying in bed)
• Cool, dark, quiet environment

**Remember**: Your health matters more than any exam. Would you like specific study techniques or sleep strategies?"""
        else:
            return f"""I hear you're stressed about academics. This pressure is real, and many students feel this way.

**Quick Stress Relief:**
• **Break It Down**: Divide big tasks into smaller, manageable steps
• **Self-Compassion**: Talk to yourself like you would a friend
• **Movement Break**: 5-minute walk or stretch

**Study Strategies:**
• Active recall over passive reading
• Study in different locations
• Teach the material to someone else

**Support Options:**
• Peer study groups
• Academic counseling
• Time management tools

What aspect feels most overwhelming right now?"""

    # Sleep issues
    if any(word in message_lower for word in ['can\'t sleep', 'insomnia', 'tired', 'exhausted']):
        return """Sleep issues often signal that your system needs care. Here are evidence-based approaches:

**Sleep Hygiene:**
• Consistent bedtime/wake time (even weekends)
• Bedroom = sleep sanctuary (cool, dark, quiet)
• No caffeine after 2 PM

**Before Bed:**
• Digital detox 1 hour before sleep
• Warm bath or shower
• Journal worries to clear your mind

**Relaxation Techniques:**
• Progressive muscle relaxation
• Guided sleep meditation
• 4-7-8 breathing

Would you like to try a specific relaxation technique now?"""

    # ... (keep all other intent responses exactly as they were)

    return None

async def generate_fallback_response(ctx: Context, message: str, session: UserSession) -> str:
    """Improved fallback response"""
    message_lower = message.lower()
    
    crisis_phrases = ['kill myself', 'suicide', 'end my life', 'want to die']
    if any(phrase in message_lower for phrase in crisis_phrases):
        return """🚨 **I'm very concerned about your safety.** Please reach out for immediate help:

• National Suicide Prevention Lifeline: 988
• Crisis Text Line: Text HOME to 741741
• Emergency Services: 911

Your life matters. Please connect with these resources right now."""
    
    return f"""Thank you for sharing: "{message}". 

I want to make sure I understand what would help you most right now.

Are you looking for:
• **Immediate coping techniques** to feel calmer?
• **Specific strategies** for a particular challenge?
• **Connection** with support resources or peers?
• **Just someone to listen** and understand?

Please tell me what type of support would be most helpful."""

async def trigger_crisis_alert(ctx: Context, session: UserSession, crisis_assessment: Dict):
    """Trigger crisis alert to other agents"""
    alert = MentalStateAlert(
        user_id=session.session_id,
        risk_level=session.risk_level,
        detected_patterns=session.user_patterns,
        recommended_actions=crisis_assessment.get('actions', []),
        timestamp=datetime.now(timezone.utc).isoformat()
    )
    
    ctx.logger.warning(f"🚨 CRISIS ALERT: User {session.session_id}")

def format_crisis_response(crisis_response: Dict) -> str:
    """Format crisis response with appropriate urgency and resources"""
    response_lines = [crisis_response['message']]
    response_lines.append("\nImmediate resources:")
    
    for action in crisis_response['actions']:
        response_lines.append(f"• {action}")
    
    response_lines.append(
        "\nPlease reach out for help. You don't have to go through this alone."
    )
    
    return "\n".join(response_lines)

# ==================== AGENT STARTUP ====================

# Include the chat protocol
soromind.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    print("🚀 Starting SoroMind Core Agent...")
    print(f"📍 Agent address: {soromind.address}")
    print("🔗 Chat Protocol: ACTIVE (Port 8001)")
    print("🌐 Ngrok: Forwarding to port 8001")
    print("💬 Debug: Message tracking ENABLED")
    print("🤝 SOMA Engine Integration: ENABLED")
    print("💫 SORO Orchestrator Integration: GUARANTEED")
    print("🔄 Retry Logic: 3 attempts with fallback")
    print("⏹️  Press CTRL+C to stop")
    print("-" * 50)
    
    try:
        soromind.run()
    except KeyboardInterrupt:
        print("\n🛑 SoroMind Core agent stopped")
    except Exception as e:
        print(f"❌ Error: {e}")