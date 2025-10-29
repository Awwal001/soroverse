#!/usr/bin/env python3
"""
SoroMind Core - Production Ready for AgentVerse
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatMessage, ChatAcknowledgement, TextContent,
    StartSessionContent, EndSessionContent
)
import uuid
from datetime import datetime, timezone
from typing import Dict, List

# ==================== CONFIGURATION ====================
# Use the same seed phrase as in your registration!
AGENT_SEED = os.getenv("AGENT_SEED_PHRASE") or os.getenv("SOROMIND_SEED")

if not AGENT_SEED:
    print("❌ ERROR: No seed phrase found!")
    print("💡 Set AGENT_SEED_PHRASE in your .env file")
    print("💡 Example: AGENT_SEED_PHRASE=your_secret_seed_phrase_here")
    sys.exit(1)

# ==================== AGENT SETUP ====================
soromind = Agent(
    name="SoroMind Core",
    seed=AGENT_SEED,
    port=8001,  # Must match your ngrok port
    endpoint=["http://localhost:8001/submit"],  # Local endpoint
    mailbox=True  # Enable AgentVerse mailbox
)

print("=" * 60)
print("🧠 SOROMIND CORE - MENTAL HEALTH AGENT")
print("=" * 60)
print(f"🔗 Agent Address: {soromind.address}")
print(f"🌐 Local URL: http://localhost:8001/submit")
print(f"🔐 Seed Phrase: {'✅ Set' if AGENT_SEED else '❌ Missing'}")
print(f"📧 Mailbox: ✅ Enabled")
print("=" * 60)

# ==================== CHAT PROTOCOL ====================
chat_proto = Protocol(name="AgentChatProtocol", version="0.3.0")

class UserSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.now(timezone.utc)
        self.message_history: List[Dict] = []
        self.risk_level = "low"

    def add_message(self, role: str, content: str):
        self.message_history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now(timezone.utc)
        })
        # Keep last 15 messages
        if len(self.message_history) > 15:
            self.message_history = self.message_history[-15:]

# Active sessions storage
user_sessions: Dict[str, UserSession] = {}

# ==================== MESSAGE HANDLING ====================
@chat_proto.on_message(model=ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages from AgentVerse"""
    ctx.logger.info(f"📨 Message from {sender[:8]}...")
    
    # Send acknowledgement
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.now(timezone.utc),
            acknowledged_msg_id=msg.msg_id
        )
    )

    user_message = ""
    session_id = None
    
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"🆕 New session with {sender[:8]}...")
            session_id = str(uuid.uuid4())
            user_sessions[session_id] = UserSession(session_id)
            continue
            
        elif isinstance(item, TextContent):
            user_message = item.text
            ctx.logger.info(f"💬 User: {user_message[:50]}...")
            
            # Get or create session
            if not session_id:
                session_id = str(uuid.uuid4())
                user_sessions[session_id] = UserSession(session_id)
            
            session = user_sessions[session_id]
            session.add_message("user", user_message)
            
            # Generate response
            response = await generate_mental_health_response(ctx, user_message, session)
            
            # Send response back
            response_msg = ChatMessage(
                timestamp=datetime.now(timezone.utc),
                msg_id=str(uuid.uuid4()),
                content=[TextContent(type="text", text=response)]
            )
            
            await ctx.send(sender, response_msg)
            session.add_message("assistant", response)
            ctx.logger.info(f"💌 Response sent to {sender[:8]}...")
            
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"🔚 Session ended with {sender[:8]}...")
            if session_id and session_id in user_sessions:
                del user_sessions[session_id]

# ==================== RESPONSE GENERATION ====================
async def generate_mental_health_response(ctx: Context, message: str, session: UserSession) -> str:
    """Generate appropriate mental health response with proper intent recognition"""
    
    message_lower = message.lower().strip()
    
    # ==================== INTENT DETECTION ====================
    
    # Crisis detection - HIGHEST PRIORITY
    crisis_phrases = [
        'want to give up', 'can\'t take it anymore', 'end it all', 
        'kill myself', 'suicide', 'harm myself', 'better off dead'
    ]
    
    if any(phrase in message_lower for phrase in crisis_phrases):
        session.risk_level = "crisis"
        ctx.logger.warning(f"🚨 CRISIS DETECTED: {message}")
        return crisis_response()
    
    # Specific request detection
    if any(word in message_lower for word in ['connect', 'resources', 'help', 'support']):
        if 'group' in message_lower or 'community' in message_lower:
            return await handle_group_connection_request(ctx, session)
        elif 'peer' in message_lower or 'person' in message_lower:
            return await handle_peer_connection_request(ctx, session)
        else:
            return resource_connection_response()
    
    if any(word in message_lower for word in ['coping', 'strategy', 'technique', 'exercise']):
        if 'breathing' in message_lower or 'box' in message_lower:
            return breathing_exercise_response()
        else:
            return coping_strategies_response(message)
    
    if any(word in message_lower for word in ['self-care', 'self care', 'care plan']):
        return self_care_plan_response()
    
    # Emotional state detection
    if any(word in message_lower for word in ['exam', 'test', 'study', 'academic']):
        return academic_stress_response(message)
    
    if any(word in message_lower for word in ['can\'t sleep', 'insomnia', 'sleep']):
        return sleep_issues_response(message)
    
    if any(word in message_lower for word in ['overwhelmed', 'too much', 'can\'t handle']):
        return overwhelmed_response(message)
    
    if any(word in message_lower for word in ['anxious', 'worry', 'nervous', 'stress']):
        return anxiety_response(message)
    
    # Default to pattern-based response
    return await generate_pattern_based_response(ctx, message, session)

async def generate_pattern_based_response(ctx: Context, message: str, session: UserSession) -> str:
    """Generate response based on detected patterns"""
    try:
        # This is where you'd call SOMA Engine for pattern analysis
        # For now, use simple pattern detection
        patterns = detect_simple_patterns(message)
        
        if 'academic_stress' in patterns and 'sleep_issues' in patterns:
            return f"""I understand you're dealing with exam stress that's affecting your sleep. This is a common pattern during intense study periods.

**Immediate Support:**
• **Study Planning**: Break your studying into 25-minute focused sessions with 5-minute breaks
• **Sleep Routine**: Try the 4-7-8 breathing technique before bed (breathe in 4s, hold 7s, out 8s)
• **Peer Connection**: Would you like me to connect you with other students managing exam stress?

**Remember**: Your worth isn't defined by your exam results. Many successful people struggled during exam periods."""

        elif 'crisis_indicators' in patterns:
            return crisis_response()
            
        else:
            return general_support_response(message)
            
    except Exception as e:
        ctx.logger.error(f"Pattern analysis error: {e}")
        return general_support_response(message)

def detect_simple_patterns(message: str) -> List[str]:
    """Simple pattern detection (replace with SOMA Engine call)"""
    patterns = []
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['exam', 'test', 'study', 'assignment']):
        patterns.append('academic_stress')
    
    if any(word in message_lower for word in ['can\'t sleep', 'insomnia', 'tired', 'exhausted']):
        patterns.append('sleep_issues')
    
    if any(word in message_lower for word in ['overwhelmed', 'too much', 'can\'t handle']):
        patterns.append('feeling_overwhelmed')
    
    if any(word in message_lower for word in ['give up', 'quit', 'can\'t take']):
        patterns.append('crisis_indicators')
    
    return patterns

# ==================== SPECIFIC RESPONSE FUNCTIONS ====================

def crisis_response() -> str:
    """Response for crisis situations"""
    return """🚨 I'm really concerned about what you're sharing. Your safety is the most important thing right now.

**IMMEDIATE HELP AVAILABLE:**
• National Suicide Prevention Lifeline: **988** or 1-800-273-8255
• Crisis Text Line: Text **HOME** to 741741
• Emergency Services: **911**

You don't have to go through this alone. Please reach out to one of these resources **right now**. They have trained professionals who can help you through this moment.

I'm here to support you, but please connect with these immediate resources first."""

def academic_stress_response(message: str) -> str:
    """Response for academic stress"""
    return f"""I hear you're feeling overwhelmed with exams. This is really common, and there are effective ways to manage this.

**For Exam Stress:**
• **Pomodoro Technique**: 25 minutes study, 5 minutes break
• **Study Planning**: Break material into smaller chunks
• **Self-Compassion**: Remember it's normal to feel stressed before exams

**Sleep Support:**
• **Digital Curfew**: No screens 1 hour before bed
• **4-7-8 Breathing**: Inhale 4s, hold 7s, exhale 8s
• **Consistent Schedule**: Same bedtime/wake time even on weekends

Would you like specific study techniques, sleep help, or to connect with other students?"""

def sleep_issues_response(message: str) -> str:
    """Response for sleep problems"""
    return """Sleep issues often accompany stress. Here are evidence-based techniques:

**Sleep Hygiene:**
• Keep your bed for sleep only (no studying in bed)
• Cool, dark, quiet room
• Consistent wake time (even weekends)

**Relaxation Techniques:**
• Progressive Muscle Relaxation
• Guided sleep meditations
• Journaling worries before bed

**Immediate Help:**
• 4-7-8 breathing exercise
• Body scan meditation

Would you like to try one of these techniques now?"""

def breathing_exercise_response() -> str:
    """Guide for box breathing"""
    return """Let's try Box Breathing together. This can calm your nervous system in minutes:

**Box Breathing Exercise:**
1. 🫳 **Breathe IN** slowly for 4 seconds...
2. ⏸️ **HOLD** your breath for 4 seconds...
3. 🫴 **Breathe OUT** slowly for 4 seconds...
4. ⏸️ **HOLD** empty for 4 seconds...

Repeat this cycle 4-5 times.

Notice how your body feels. Would you like to continue with another cycle, or try a different technique?"""

async def handle_group_connection_request(ctx: Context, session: UserSession) -> str:
    """Handle requests to connect with groups"""
    # This would call PSN Connect in production
    ctx.logger.info("🤝 Group connection request - would call PSN Connect")
    return """I can help connect you with supportive groups:

**Available Groups:**
• **Academic Stress Management** (Mondays 6 PM)
• **Anxiety Support Circle** (Tues/Thurs 7 PM) 
• **Mindfulness & Meditation** (Daily 8 AM)

These groups are facilitated by trained peers who understand what you're going through.

Would you like me to check availability for any of these?"""

async def handle_peer_connection_request(ctx: Context, session: UserSession) -> str:
    """Handle requests for peer connection"""
    # This would call PSN Connect in production
    ctx.logger.info("👥 Peer connection request - would call PSN Connect")
    return """I can connect you with a peer supporter who understands exam stress and sleep issues.

**Available Peer Supporters:**
• **Alex** - Experienced with academic stress, available evenings
• **Taylor** - Specializes in anxiety management, flexible hours
• **Jordan** - Great with sleep issues and study planning

They've helped others through similar challenges. Would you like an introduction?"""

def resource_connection_response() -> str:
    """Response for general resource requests"""
    return """I can connect you with various mental health resources:

**Immediate Support:**
• Crisis Hotline: 988 (24/7)
• Online therapy platforms with immediate sessions

**Ongoing Support:**
• University counseling services (if applicable)
• Community mental health centers
• Support groups for stress and anxiety

**Self-Help Resources:**
• Mental health apps (Calm, Headspace)
• Online CBT programs
• Wellness workshops

What type of support are you looking for specifically?"""

def coping_strategies_response(message: str) -> str:
    """Response for coping strategy requests"""
    return """Here are some effective coping strategies for stress:

**Quick Relief (5 minutes or less):**
• Box Breathing exercise
• 5-4-3-2-1 Grounding technique
• Progressive Muscle Relaxation

**Daily Practices:**
• Mindful walking
• Gratitude journaling
• Scheduled worry time

**Academic Specific:**
• Study scheduling with breaks
• Task prioritization
• Self-compassion breaks

Would you like to try one of these now, or learn more about a specific technique?"""

def self_care_plan_response() -> str:
    """Response for self-care plan requests"""
    return """Let's build a simple self-care plan together:

**Daily Foundation:**
• Sleep: Aim for 7-8 hours consistent schedule
• Nutrition: Regular meals, stay hydrated
• Movement: 20-30 minutes daily (walking counts!)

**Stress Management:**
• Morning: 5 minutes of deep breathing
• Study breaks: Every 45-60 minutes
• Evening: Digital detox 1 hour before bed

**Emotional Support:**
• Connect with one supportive person daily
• Acknowledge small accomplishments
• Practice self-compassion

Would you like to customize any part of this plan for your situation?"""

def overwhelmed_response(message: str) -> str:
    """Response for feeling overwhelmed"""
    return """Feeling overwhelmed is your system saying "too much, too fast." Let's break this down:

**Right Now:**
• Stop and take 3 deep breaths
• Name 3 things you can see around you
• Drink a glass of water

**Next Steps:**
• What's the ONE most urgent thing?
• Can anything be postponed or delegated?
• What support do you need right now?

**Remember**: You don't have to solve everything at once. Let's focus on just the next small step.

What feels most manageable to address first?"""

def general_support_response(message: str) -> str:
    """Improved general response"""
    return f"""Thank you for sharing: "{message}". 

I want to make sure I understand exactly what would help you most right now.

Are you looking for:
• **Immediate coping techniques** to feel calmer?
• **Study/sleep strategies** specifically for exam period?
• **Connection** with peers or support groups?
• **Professional resources** for ongoing support?

Please tell me what type of support would be most helpful at this moment."""

# ==================== PROTOCOL SETUP ====================
soromind.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    print("🚀 Starting SoroMind Core Agent...")
    print("💡 Make sure ngrok is running: ngrok http 8001")
    print("📋 Registration: python3 register_agent.py")
    print("⏹️  Press CTRL+C to stop")
    print("-" * 60)
    
    try:
        soromind.run()
    except KeyboardInterrupt:
        print("\n🛑 SoroMind agent stopped gracefully")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Troubleshooting:")
        print("   - Check if port 8001 is available")
        print("   - Verify AGENT_SEED_PHRASE in .env")
        print("   - Ensure ngrok is running")