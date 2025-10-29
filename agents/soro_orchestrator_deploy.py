#!/usr/bin/env python3
"""
SORO Orchestrator - Deployment Version for AgentVerse
"""

import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, timezone
from typing import List, Dict, Any
from uagents import Agent, Context, Protocol, Model

# Define data models
class RiskLevel:
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRISIS = "crisis"

class InterventionRequest(Model):
    user_id: str
    user_state: str
    patterns: List[str]
    risk_level: str
    timestamp: datetime

class InterventionResponse(Model):
    techniques: List[str]
    reasoning: str
    confidence: float
    duration_minutes: int
    resources: List[str]

class MentalStateAlert(Model):
    user_id: str
    risk_level: str
    detected_patterns: List[str]
    recommended_actions: List[str]
    timestamp: datetime

class PatternAnalysisResponse(Model):
    patterns: List[str]
    confidence: float
    risk_assessment: str
    suggested_interventions: List[str]

# Mock MeTTa Manager
class MeTTaManager:
    def get_interventions_for_pattern(self, pattern: str) -> List[Dict[str, Any]]:
        """Mock implementation - in production would query MeTTa knowledge graph"""
        interventions_db = {
            'anxiety': [
                {'name': 'Box Breathing', 'effectiveness': 0.85, 'details': {'technique': 'Breathe in 4s, hold 4s, out 4s, hold 4s'}},
                {'name': '5-4-3-2-1 Grounding', 'effectiveness': 0.78, 'details': {'technique': 'Notice 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste'}},
                {'name': 'Progressive Muscle Relaxation', 'effectiveness': 0.72, 'details': {'technique': 'Tense and release each muscle group from toes to head'}}
            ],
            'depression': [
                {'name': 'Behavioral Activation', 'effectiveness': 0.82, 'details': {'technique': 'Schedule and engage in rewarding activities'}},
                {'name': 'Gratitude Journaling', 'effectiveness': 0.75, 'details': {'technique': 'Write down three things you are grateful for each day'}},
                {'name': 'Social Connection', 'effectiveness': 0.80, 'details': {'technique': 'Reach out to supportive friends or family'}}
            ],
            'stress': [
                {'name': 'Mindful Breathing', 'effectiveness': 0.79, 'details': {'technique': 'Focus on breath for 5-10 minutes'}},
                {'name': 'Time Management', 'effectiveness': 0.76, 'details': {'technique': 'Break tasks into smaller, manageable steps'}},
                {'name': 'Physical Activity', 'effectiveness': 0.81, 'details': {'technique': '20-30 minutes of moderate exercise'}}
            ],
            'loneliness': [
                {'name': 'Community Engagement', 'effectiveness': 0.77, 'details': {'technique': 'Join local groups or online communities'}},
                {'name': 'Volunteer Work', 'effectiveness': 0.74, 'details': {'technique': 'Help others to build connections and purpose'}},
                {'name': 'Skill Development', 'effectiveness': 0.70, 'details': {'technique': 'Learn new skills in group settings'}}
            ]
        }
        
        return interventions_db.get(pattern, [
            {'name': 'Mindful Breathing', 'effectiveness': 0.7, 'details': {'technique': 'Basic breathing exercise'}}
        ])

# Initialize components
metta_manager = MeTTaManager()

# SORO Orchestrator Agent
soro_orchestrator = Agent(
    name="SORO Orchestrator",
    seed=os.getenv("SORO_ORCHESTRATOR_SEED", "soro_orchestrator_secret_003"),
    port=8004,  # Different port from others
    endpoint=["http://localhost:8004/submit"],
    mailbox=True
)

print("=" * 50)
print("💫 SORO ORCHESTRATOR - INTERVENTION COORDINATION")
print("=" * 50)
print(f"📍 Agent Address: {soro_orchestrator.address}")
print(f"🌐 Local URL: http://localhost:8004/submit")
print("=" * 50)

# Intervention protocol
intervention_proto = Protocol(name="InterventionOrchestration", version="1.0.0")

@intervention_proto.on_message(model=InterventionRequest)
async def handle_intervention_request(ctx: Context, sender: str, msg: InterventionRequest):
    """Handle intervention requests and coordinate appropriate responses"""
    ctx.logger.info(f"🎯 Intervention request for risk: {msg.risk_level}")
    ctx.logger.info(f"📊 User state: {msg.user_state[:50]}...")
    ctx.logger.info(f"🔍 Patterns: {msg.patterns}")
    
    try:
        # Get evidence-based interventions from MeTTa
        interventions = get_interventions_for_state(
            msg.user_state, 
            msg.patterns, 
            msg.risk_level
        )
        
        # For medium/high risk, consider additional coordination
        if msg.risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH]:
            ctx.logger.info("🤝 Additional support coordination recommended")
        
        response = InterventionResponse(
            techniques=interventions['techniques'],
            reasoning=interventions['reasoning'],
            confidence=interventions['confidence'],
            duration_minutes=interventions['duration'],
            resources=interventions['resources']
        )
        
        await ctx.send(sender, response)
        ctx.logger.info(f"✅ Sent intervention with {len(interventions['techniques'])} techniques")
        
    except Exception as e:
        ctx.logger.error(f"❌ Intervention error: {e}")
        fallback_response = InterventionResponse(
            techniques=["Mindful breathing", "Grounding exercise"],
            reasoning="Basic stress reduction techniques",
            confidence=0.7,
            duration_minutes=5,
            resources=["Breathing exercise guide", "Grounding techniques"]
        )
        await ctx.send(sender, fallback_response)

@intervention_proto.on_message(model=MentalStateAlert)
async def handle_crisis_intervention(ctx: Context, sender: str, msg: MentalStateAlert):
    """Handle crisis situations with immediate interventions"""
    ctx.logger.warning(f"🚨 CRISIS INTERVENTION for user {msg.user_id[:8]}...")
    ctx.logger.warning(f"⚠️ Risk level: {msg.risk_level}")
    
    # Get crisis-specific interventions
    crisis_interventions = get_crisis_interventions(msg.risk_level)
    
    ctx.logger.info(f"🛟 Immediate actions: {msg.recommended_actions}")
    ctx.logger.info(f"🎯 Crisis protocols: {crisis_interventions}")
    
    # Log coordination steps
    if msg.risk_level == RiskLevel.CRISIS:
        ctx.logger.warning("🚑 PROFESSIONAL INTERVENTION REQUIRED - Coordinating emergency response")
    elif msg.risk_level == RiskLevel.HIGH:
        ctx.logger.warning("🔄 Coordinating multi-agent support response")

@intervention_proto.on_message(model=PatternAnalysisResponse)
async def handle_pattern_analysis(ctx: Context, sender: str, msg: PatternAnalysisResponse):
    """Handle pattern analysis results to preemptively suggest interventions"""
    ctx.logger.info(f"🔍 Pattern analysis received: {len(msg.patterns)} patterns")
    ctx.logger.info(f"📈 Risk assessment: {msg.risk_assessment}")
    ctx.logger.info(f"💡 Suggested interventions: {msg.suggested_interventions[:2]}...")
    
    # Store pattern analysis for proactive support
    if msg.risk_assessment in [RiskLevel.HIGH, RiskLevel.CRISIS]:
        ctx.logger.warning("⚠️ High-risk patterns - preparing proactive interventions")
        # In production: Schedule check-ins, prepare resources, notify support network

def get_interventions_for_state(
    user_state: str, 
    patterns: List[str], 
    risk_level: str
) -> Dict[str, Any]:
    """Get appropriate interventions based on user state and patterns"""
    
    interventions = {
        'techniques': [],
        'reasoning': "",
        'confidence': 0.0,
        'duration': 15,
        'resources': []
    }
    
    try:
        # Get interventions from MeTTa for each pattern
        all_interventions = []
        for pattern in patterns[:2]:  # Limit to top 2 patterns
            pattern_interventions = metta_manager.get_interventions_for_pattern(pattern)
            all_interventions.extend(pattern_interventions)
        
        # Sort by effectiveness and select top 3
        all_interventions.sort(key=lambda x: x.get('effectiveness', 0), reverse=True)
        top_interventions = all_interventions[:3]
        
        # Build response
        interventions['techniques'] = [
            interv['name'] for interv in top_interventions
        ]
        
        if top_interventions:
            interventions['confidence'] = top_interventions[0].get('effectiveness', 0.7)
            interventions['reasoning'] = (
                f"Based on patterns of {', '.join(patterns[:2])}, "
                f"these evidence-based techniques have shown effectiveness "
                f"in similar situations (confidence: {interventions['confidence']:.0%})."
            )
            
            # Add resources from intervention details
            for interv in top_interventions:
                if 'details' in interv and 'technique' in interv['details']:
                    interventions['resources'].append(
                        f"{interv['name']}: {interv['details']['technique']}"
                    )
        
        # Adjust for risk level
        if risk_level == RiskLevel.HIGH:
            interventions['techniques'].insert(0, "Immediate grounding exercise")
            interventions['duration'] = 10
            interventions['reasoning'] = "HIGH RISK - " + interventions['reasoning']
        elif risk_level == RiskLevel.CRISIS:
            interventions['techniques'] = ["CRISIS PROTOCOL ACTIVATION"]
            interventions['reasoning'] = "IMMEDIATE PROFESSIONAL SUPPORT REQUIRED"
            interventions['resources'] = [
                "National Suicide Prevention Lifeline: 988",
                "Crisis Text Line: Text HOME to 741741",
                "Emergency Services: 911"
            ]
            interventions['confidence'] = 1.0
            
    except Exception as e:
        print(f"Error getting interventions: {e}")
        # Fallback interventions
        interventions['techniques'] = ["Mindful breathing", "Progressive relaxation"]
        interventions['reasoning'] = "Basic stress reduction techniques"
        interventions['confidence'] = 0.7
        interventions['resources'] = ["Breathing exercise guide"]
    
    return interventions

def get_crisis_interventions(risk_level: str) -> List[str]:
    """Get crisis-specific interventions"""
    crisis_protocols = {
        RiskLevel.HIGH: [
            "Immediate grounding techniques",
            "Crisis resource connection", 
            "Safety planning",
            "Support network activation"
        ],
        RiskLevel.CRISIS: [
            "EMERGENCY PROTOCOL ACTIVATION",
            "Professional crisis support",
            "Immediate human connection",
            "Continuous monitoring"
        ]
    }
    
    return crisis_protocols.get(risk_level, ["Monitoring and support"])

# Include protocol
soro_orchestrator.include(intervention_proto, publish_manifest=True)

if __name__ == "__main__":
    print("🚀 Starting SORO Orchestrator Agent...")
    print("🎯 Intervention Coordination & Crisis Management")
    print("💡 Make sure to run ngrok for port 8004")
    print("⏹️  Press CTRL+C to stop")
    print("-" * 50)
    
    try:
        soro_orchestrator.run()
    except KeyboardInterrupt:
        print("\n🛑 SORO Orchestrator agent stopped")
    except Exception as e:
        print(f"❌ Error: {e}")