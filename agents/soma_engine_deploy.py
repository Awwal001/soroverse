#!/usr/bin/env python3
"""
SOMA Engine - Deployment Version for AgentVerse
"""

import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, timezone
from typing import Dict, List, Optional
from uagents import Agent, Context, Protocol, Model

# Initialize components (simplified for deployment)
class MeTTaManager:
    def query_emotional_patterns(self, emotion: str) -> List[str]:
        return [f"{emotion}_pattern", f"cognitive_{emotion}"]

class ASIClient:
    async def analyze_mental_patterns(self, message: str, history: List[str]):
        return type('obj', (object,), {
            'patterns': ['thought_pattern', 'emotional_trend'],
            'confidence': 0.85
        })()

metta_manager = MeTTaManager()
asi_client = ASIClient()

# Define data models
class RiskLevel:
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRISIS = "crisis"

class PatternAnalysisRequest(Model):
    user_message: str
    session_history: List[str]
    user_id: Optional[str] = None

class PatternAnalysisResponse(Model):
    patterns: List[str]
    confidence: float
    risk_assessment: str
    suggested_interventions: List[str]

class MentalStateAlert(Model):
    user_id: str
    risk_level: str
    detected_patterns: List[str]
    recommended_actions: List[str]
    timestamp: datetime

# SOMA Engine Agent
soma_engine = Agent(
    name="SOMA Engine",
    seed=os.getenv("SOMA_ENGINE_SEED", "soma_engine_secret_phrase_002"),
    port=8002,  # Different port from SoroMind
    endpoint=["http://localhost:8002/submit"],
    mailbox=True
)

print("=" * 50)
print("🧠 SOMA ENGINE - PATTERN ANALYSIS AGENT")
print("=" * 50)
print(f"📍 Agent Address: {soma_engine.address}")
print(f"🌐 Local URL: http://localhost:8002/submit")
print("=" * 50)

# Protocol for pattern analysis
analysis_proto = Protocol(name="PatternAnalysis", version="1.0.0")

@analysis_proto.on_message(model=PatternAnalysisRequest)
async def handle_pattern_analysis(ctx: Context, sender: str, msg: PatternAnalysisRequest):
    """Handle pattern analysis requests from other agents"""
    ctx.logger.info(f"🔍 Pattern analysis request from {sender[:8]}...")
    
    try:
        # Simulate ASI:One analysis
        analysis = await asi_client.analyze_mental_patterns(
            msg.user_message, 
            msg.session_history
        )
        
        # Enhance with MeTTa knowledge
        enhanced_patterns = await enhance_with_metta_knowledge(analysis.patterns, msg.user_message)
        
        # Determine risk level
        risk_level = assess_risk_level(enhanced_patterns, msg.user_message)
        
        # Generate interventions
        interventions = generate_interventions(enhanced_patterns, risk_level)
        
        # Send response back
        response = PatternAnalysisResponse(
            patterns=enhanced_patterns,
            confidence=analysis.confidence,
            risk_assessment=risk_level,
            suggested_interventions=interventions
        )
        
        await ctx.send(sender, response)
        ctx.logger.info(f"✅ Analysis completed - {len(enhanced_patterns)} patterns found")
        
    except Exception as e:
        ctx.logger.error(f"❌ Analysis error: {e}")
        error_response = PatternAnalysisResponse(
            patterns=[],
            confidence=0.0,
            risk_assessment=RiskLevel.LOW,
            suggested_interventions=[]
        )
        await ctx.send(sender, error_response)

@analysis_proto.on_message(model=MentalStateAlert)
async def handle_mental_state_alert(ctx: Context, sender: str, msg: MentalStateAlert):
    """Handle mental state alerts for crisis situations"""
    ctx.logger.warning(f"🚨 CRISIS ALERT from {sender[:8]}: Risk level {msg.risk_level}")
    
    ctx.logger.info(f"📊 User {msg.user_id} patterns: {msg.detected_patterns}")
    ctx.logger.info(f"🛟 Recommended actions: {msg.recommended_actions}")
    
    # Trigger enhanced monitoring for high-risk cases
    if msg.risk_level in [RiskLevel.HIGH, RiskLevel.CRISIS]:
        await trigger_enhanced_monitoring(ctx, msg.user_id)

async def enhance_with_metta_knowledge(patterns: List[str], user_message: str) -> List[str]:
    """Enhance pattern analysis with MeTTa knowledge graph insights"""
    enhanced_patterns = patterns.copy()
    
    emotions = extract_emotions_from_text(user_message)
    
    for emotion in emotions:
        emotion_patterns = metta_manager.query_emotional_patterns(emotion)
        enhanced_patterns.extend(emotion_patterns)
    
    # Add cognitive patterns based on message characteristics
    if len(user_message) > 100:
        enhanced_patterns.append("detailed_expression")
    if '?' in user_message:
        enhanced_patterns.append("seeking_clarity")
    if '!' in user_message:
        enhanced_patterns.append("emotional_intensity")
    
    return list(set(enhanced_patterns))

def extract_emotions_from_text(text: str) -> List[str]:
    """Extract emotions from text"""
    emotions = []
    text_lower = text.lower()
    
    emotion_keywords = {
        'anxiety': ['anxious', 'worried', 'nervous', 'panic', 'overwhelmed', 'stressed'],
        'depression': ['sad', 'depressed', 'hopeless', 'empty', 'numb', 'tired'],
        'anger': ['angry', 'frustrated', 'irritated', 'mad', 'annoyed'],
        'fear': ['scared', 'afraid', 'fearful', 'terrified'],
        'loneliness': ['alone', 'lonely', 'isolated', 'abandoned']
    }
    
    for emotion, keywords in emotion_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            emotions.append(emotion)
    
    return emotions

def assess_risk_level(patterns: List[str], message: str) -> str:
    """Assess risk level based on patterns and message content"""
    high_risk_indicators = ['suicide', 'harm', 'kill myself', 'end it all']
    message_lower = message.lower()
    
    if any(indicator in message_lower for indicator in high_risk_indicators):
        return RiskLevel.CRISIS
    
    if 'anxiety' in patterns and 'depression' in patterns:
        return RiskLevel.HIGH
    
    if len(patterns) >= 3:
        return RiskLevel.MEDIUM
    
    return RiskLevel.LOW

def generate_interventions(patterns: List[str], risk_level: str) -> List[str]:
    """Generate appropriate interventions based on patterns and risk"""
    interventions = []
    
    if risk_level == RiskLevel.CRISIS:
        interventions.extend(["Immediate crisis intervention", "Emergency contact"])
    
    if 'anxiety' in patterns:
        interventions.extend(["Breathing exercises", "Grounding techniques", "Mindfulness"])
    
    if 'depression' in patterns:
        interventions.extend(["Behavioral activation", "Social connection", "Physical activity"])
    
    if 'loneliness' in patterns:
        interventions.extend(["Peer support groups", "Community engagement"])
    
    # Always include basic support
    interventions.append("Professional consultation")
    
    return interventions[:5]  # Return top 5 interventions

async def trigger_enhanced_monitoring(ctx: Context, user_id: str):
    """Trigger enhanced monitoring for high-risk users"""
    ctx.logger.info(f"🔒 Starting enhanced monitoring for user {user_id}")
    # In production: Increase check-ins, notify moderators, prepare resources

# Include the protocol
soma_engine.include(analysis_proto, publish_manifest=True)

if __name__ == "__main__":
    print("🚀 Starting SOMA Engine Agent...")
    print("🔍 Pattern Analysis & Cognitive Mapping")
    print("💡 Make sure to run ngrok for port 8002")
    print("⏹️  Press CTRL+C to stop")
    print("-" * 50)
    
    try:
        soma_engine.run()
    except KeyboardInterrupt:
        print("\n🛑 SOMA Engine agent stopped")
    except Exception as e:
        print(f"❌ Error: {e}")