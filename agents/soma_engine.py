#!/usr/bin/env python3

import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from datetime import datetime, timezone
from typing import Dict, List, Optional

from uagents import Agent, Context, Protocol, Model
# Remove this import - we don't need the chat protocol in SOMA Engine
# from uagents_core.contrib.protocols.chat import chat_protocol_spec

from models.data_models import (
    PatternAnalysisRequest, PatternAnalysisResponse, 
    MentalStateAlert, RiskLevel
)
from knowledge.metta_manager import MeTTaManager
from utils.asi_client import ASIClient

# Initialize components
metta_manager = MeTTaManager()
asi_client = ASIClient()

# SOMA Engine Agent for deep pattern analysis
soma_engine = Agent(
    name="SOMA Engine",
    seed=os.getenv("SOMA_ENGINE_SEED", "soma_engine_secret_phrase_002"),
    port=8002,
    endpoint=["http://localhost:8002/submit"],
    mailbox=True
)

# Protocol for pattern analysis requests
analysis_proto = Protocol(name="PatternAnalysis", version="1.0.0")

@analysis_proto.on_message(PatternAnalysisRequest)
async def handle_pattern_analysis(ctx: Context, sender: str, msg: PatternAnalysisRequest):
    """Handle pattern analysis requests from other agents"""
    ctx.logger.info(f"Received pattern analysis request from {sender}")
    
    try:
        # Use ASI:One for deep pattern analysis
        analysis = await asi_client.analyze_mental_patterns(
            msg.user_message, 
            msg.session_history
        )
        
        # Enhance with MeTTa knowledge graph insights
        enhanced_patterns = await enhance_with_metta_knowledge(analysis.patterns, msg.user_message)
        analysis.patterns = enhanced_patterns
        
        # Send response back
        await ctx.send(sender, analysis)
        
        ctx.logger.info(f"Pattern analysis completed for session")
        
    except Exception as e:
        ctx.logger.error(f"Error in pattern analysis: {e}")
        # Send error response
        error_response = PatternAnalysisResponse(
            patterns=[],
            confidence=0.0,
            risk_assessment=RiskLevel.LOW,
            suggested_interventions=[]
        )
        await ctx.send(sender, error_response)

@analysis_proto.on_message(MentalStateAlert)
async def handle_mental_state_alert(ctx: Context, sender: str, msg: MentalStateAlert):
    """Handle mental state alerts for crisis situations"""
    ctx.logger.warning(f"CRISIS ALERT from {sender}: Risk level {msg.risk_level}")
    
    # Log the alert for monitoring
    ctx.logger.info(f"User {msg.user_id} patterns: {msg.detected_patterns}")
    ctx.logger.info(f"Recommended actions: {msg.recommended_actions}")
    
    # In full implementation, this would trigger additional crisis protocols
    if msg.risk_level in [RiskLevel.HIGH, RiskLevel.CRISIS]:
        await trigger_enhanced_monitoring(ctx, msg.user_id)

async def enhance_with_metta_knowledge(patterns: List[str], user_message: str) -> List[str]:
    """Enhance pattern analysis with MeTTa knowledge graph insights"""
    enhanced_patterns = patterns.copy()
    
    # Query MeTTa for additional patterns based on message content
    try:
        # Extract emotions from message (simplified)
        emotions = extract_emotions_from_text(user_message)
        
        for emotion in emotions:
            # Get patterns associated with this emotion
            emotion_patterns = metta_manager.query_emotional_patterns(emotion)
            enhanced_patterns.extend(emotion_patterns)
        
        # Remove duplicates and return
        return list(set(enhanced_patterns))
        
    except Exception as e:
        print(f"Error enhancing with MeTTa: {e}")
        return patterns

def extract_emotions_from_text(text: str) -> List[str]:
    """Extract emotions from text (simplified implementation)"""
    emotions = []
    text_lower = text.lower()
    
    emotion_keywords = {
        'anxiety': ['anxious', 'worried', 'nervous', 'panic', 'overwhelmed'],
        'depression': ['sad', 'depressed', 'hopeless', 'empty', 'numb'],
        'stress': ['stressed', 'pressure', 'burnout', 'exhausted'],
        'anger': ['angry', 'frustrated', 'irritated', 'mad'],
        'fear': ['scared', 'afraid', 'fearful', 'terrified']
    }
    
    for emotion, keywords in emotion_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            emotions.append(emotion)
    
    return emotions

async def trigger_enhanced_monitoring(ctx: Context, user_id: str):
    """Trigger enhanced monitoring for high-risk users"""
    ctx.logger.info(f"Starting enhanced monitoring for user {user_id}")
    
    # In full implementation, this would:
    # 1. Increase check-in frequency
    # 2. Notify human moderators
    # 3. Prepare emergency resources
    # 4. Coordinate with PSN Connect for immediate peer support

# Include only the analysis protocol (remove the chat protocol)
soma_engine.include(analysis_proto, publish_manifest=True)

# REMOVED: chat_proto inclusion since SoroMind already handles chat

if __name__ == "__main__":
    print("🧠 Starting SOMA Engine Agent...")
    print(f"📍 Agent address: {soma_engine.address}")
    print("🔍 Pattern analysis and cognitive mapping enabled")
    soma_engine.run()