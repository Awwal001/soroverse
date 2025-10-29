#!/usr/bin/env python3


import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from datetime import datetime, timezone
from typing import List, Dict, Any

from uagents import Agent, Context, Protocol, Model

from models.data_models import (
    InterventionRequest, InterventionResponse, MentalStateAlert,
    RiskLevel, PeerMatchRequest, PatternAnalysisResponse
)
from knowledge.metta_manager import MeTTaManager

# Rest of your existing code...

# Initialize MeTTa manager
metta_manager = MeTTaManager()

# SORO Orchestrator Agent for intervention coordination
soro_orchestrator = Agent(
    name="SORO Orchestrator",
    seed=os.getenv("SORO_ORCHESTRATOR_SEED", "soro_orchestrator_secret_003"),
    port=8003,
    endpoint=["http://localhost:8003/submit"],
    mailbox=True
)

# Intervention protocol
intervention_proto = Protocol(name="InterventionOrchestration", version="1.0.0")

# Mock peer support agent address (would be discovered in real implementation)
PSN_CONNECT_ADDRESS = "agent1q2w3e4r5t6y7u8i9o0p"  # Placeholder

@intervention_proto.on_message(InterventionRequest)
async def handle_intervention_request(ctx: Context, sender: str, msg: InterventionRequest):
    """Handle intervention requests and coordinate appropriate responses"""
    ctx.logger.info(f"Received intervention request for risk level: {msg.risk_level}")
    
    try:
        # Get evidence-based interventions from MeTTa
        interventions = get_interventions_for_state(
            msg.user_state, 
            msg.patterns, 
            msg.risk_level
        )
        
        # For medium/high risk, consider peer support
        peer_recommendation = msg.risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH]
        
        if peer_recommendation:
            # In full implementation, this would send to PSN Connect
            ctx.logger.info("Peer support recommended for this intervention")
        
        response = InterventionResponse(
            techniques=interventions['techniques'],
            reasoning=interventions['reasoning'],
            confidence=interventions['confidence'],
            duration_minutes=interventions['duration'],
            resources=interventions['resources']
        )
        
        await ctx.send(sender, response)
        ctx.logger.info("Intervention response sent successfully")
        
    except Exception as e:
        ctx.logger.error(f"Error handling intervention request: {e}")
        # Send fallback response
        fallback_response = InterventionResponse(
            techniques=["Mindful breathing", "Grounding exercise"],
            reasoning="Basic stress reduction techniques",
            confidence=0.7,
            duration_minutes=5,
            resources=["Breathing exercise guide", "Grounding techniques"]
        )
        await ctx.send(sender, fallback_response)

@intervention_proto.on_message(MentalStateAlert)
async def handle_crisis_intervention(ctx: Context, sender: str, msg: MentalStateAlert):
    """Handle crisis situations with immediate interventions"""
    ctx.logger.warning(f"CRISIS INTERVENTION needed for user {msg.user_id}")
    
    # Get crisis-specific interventions
    crisis_interventions = get_crisis_interventions(msg.risk_level)
    
    # Log immediate actions
    ctx.logger.info(f"Immediate actions: {msg.recommended_actions}")
    ctx.logger.info(f"Crisis interventions: {crisis_interventions}")
    
    # In full implementation, this would coordinate with all relevant agents

@intervention_proto.on_message(PatternAnalysisResponse)
async def handle_pattern_analysis(ctx: Context, sender: str, msg: PatternAnalysisResponse):
    """Handle pattern analysis results to preemptively suggest interventions"""
    ctx.logger.info(f"Received pattern analysis with {len(msg.patterns)} patterns")
    
    # Store pattern analysis for future intervention planning
    # This enables proactive support based on user patterns
    
    if msg.risk_assessment in [RiskLevel.HIGH, RiskLevel.CRISIS]:
        ctx.logger.warning("High-risk patterns detected, preparing interventions")

def get_interventions_for_state(
    user_state: str, 
    patterns: List[str], 
    risk_level: RiskLevel
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
                f"in similar situations."
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
        elif risk_level == RiskLevel.CRISIS:
            interventions['techniques'] = ["Crisis protocol activation"]
            interventions['reasoning'] = "Immediate professional support required"
            interventions['resources'] = [
                "National Suicide Prevention Lifeline: 988",
                "Crisis Text Line: Text HOME to 741741"
            ]
            
    except Exception as e:
        ctx.logger.error(f"Error getting interventions: {e}")
        # Fallback interventions
        interventions['techniques'] = ["Mindful breathing", "Progressive relaxation"]
        interventions['reasoning'] = "Basic stress reduction techniques"
        interventions['confidence'] = 0.7
        interventions['resources'] = ["Breathing exercise guide"]
    
    return interventions

def get_crisis_interventions(risk_level: RiskLevel) -> List[str]:
    """Get crisis-specific interventions"""
    crisis_protocols = {
        RiskLevel.HIGH: [
            "Immediate grounding techniques",
            "Crisis resource connection",
            "Safety planning"
        ],
        RiskLevel.CRISIS: [
            "Emergency protocol activation",
            "Professional crisis support",
            "Immediate human connection"
        ]
    }
    
    return crisis_protocols.get(risk_level, ["Monitoring and support"])

# Include protocol
soro_orchestrator.include(intervention_proto, publish_manifest=True)

if __name__ == "__main__":
    print("💫 Starting SORO Orchestrator Agent...")
    print(f"📍 Agent address: {soro_orchestrator.address}")
    print("🎯 Intervention coordination and crisis management enabled")
    soro_orchestrator.run()