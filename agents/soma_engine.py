#!/usr/bin/env python3
"""
SOMA Engine - COMPLETE FIXED VERSION
"""

import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from datetime import datetime, timezone
from typing import List
from uagents import Agent, Context, Protocol

# Import COMMON models
from common_models import PatternAnalysisRequest, PatternAnalysisResponse, RiskLevel

print("✅ SOMA Engine - Common models imported")

# Mock implementations
class MeTTaManager:
    def query_emotional_patterns(self, emotion: str) -> List[str]:
        patterns_db = {
            'anxiety': ['perfectionism', 'catastrophizing', 'overgeneralization'],
            'depression': ['black_white_thinking', 'emotional_reasoning', 'personalization'],
            'stress': ['rushing_pattern', 'pressure_response', 'burnout_tendency'],
        }
        return patterns_db.get(emotion, [f"{emotion}_pattern"])

class ASIClient:
    async def analyze_mental_patterns(self, message: str, history: List[str]):
        patterns = []
        emotions = []
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['exam', 'test', 'study', 'academic']):
            patterns.extend(['academic_perfectionism', 'performance_anxiety'])
            emotions.append('anxiety')
        if any(word in message_lower for word in ['anxious', 'worry', 'nervous']):
            patterns.extend(['catastrophizing', 'future_worry'])
            emotions.append('anxiety')
        if any(word in message_lower for word in ['stress', 'pressure']):
            patterns.extend(['task_overload', 'boundary_issues'])
            emotions.append('stress')
        
        enhanced_patterns = patterns.copy()
        if 'academic' in message_lower:
            enhanced_patterns.append('academic_stress')
        if 'peer' in message_lower or 'group' in message_lower:
            enhanced_patterns.append('social_support_seeking')
        
        return type('obj', (object,), {
            'patterns': patterns if patterns else ['general_stress_pattern'],
            'emotions': emotions if emotions else ['concern'],
            'risk_level': RiskLevel.LOW,
            'enhanced_patterns': enhanced_patterns,
            'confidence': 0.85
        })()

# Initialize
metta_manager = MeTTaManager()
asi_client = ASIClient()

# Agent
soma_engine = Agent(
    name="SOMA Engine",
    seed=os.getenv("SOMA_ENGINE_SEED", "soma_engine_secret_phrase_002"),
    port=8002,
    endpoint=["http://localhost:8002/submit"],
    mailbox=True
)

print("=" * 60)
print("🧠 SOMA ENGINE - FIXED WITH COMMON MODELS")
print("=" * 60)
print(f"📍 Agent Address: {soma_engine.address}")

# Protocol
analysis_proto = Protocol(name="PatternAnalysis", version="1.0.0")

@analysis_proto.on_message(PatternAnalysisRequest)
async def handle_pattern_analysis(ctx: Context, sender: str, msg: PatternAnalysisRequest):
    print(f"🎯 SOMA ENGINE: Analysis request from {sender[:16]}...")
    print(f"   📝 Message: '{msg.user_message[:50]}...'")
    
    try:
        analysis_result = await asi_client.analyze_mental_patterns(
            msg.user_message, 
            msg.session_history
        )
        
        response = PatternAnalysisResponse(
            user_id=msg.user_id,
            patterns=analysis_result.patterns,
            emotions=analysis_result.emotions,
            risk_level=analysis_result.risk_level,
            enhanced_patterns=analysis_result.enhanced_patterns,
            analysis_confidence=analysis_result.confidence
        )
        
        await ctx.send(sender, response)
        print(f"✅ SOMA ENGINE: Analysis COMPLETED")
        print(f"   📊 Patterns: {analysis_result.patterns}")
        print(f"   🎭 Emotions: {analysis_result.emotions}")
        print(f"   🔍 Enhanced: {analysis_result.enhanced_patterns}")
        
    except Exception as e:
        print(f"❌ SOMA: Analysis failed - {e}")
        error_response = PatternAnalysisResponse(
            user_id=msg.user_id,
            patterns=['analysis_error'],
            emotions=[],
            risk_level=RiskLevel.LOW,
            enhanced_patterns=[],
            analysis_confidence=0.0
        )
        await ctx.send(sender, error_response)

soma_engine.include(analysis_proto, publish_manifest=True)

if __name__ == "__main__":
    print("🚀 Starting SOMA Engine...")
    soma_engine.run()