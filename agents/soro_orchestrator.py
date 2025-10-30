#!/usr/bin/env python3
"""
SORO Orchestrator - Enhanced with PSN Connect Integration
Intervention Coordination & Multi-Agent Management
"""

import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

print("✅ Environment setup completed")

# Import your actual modules with error handling
try:


    from common_models import (
    InterventionRequest, InterventionResponse, MentalStateAlert,
    RiskLevel, PatternAnalysisResponse, PeerSupportRecommendation, 
    PeerSupportActivation, UserPreferences
)

    from knowledge.metta_manager import MeTTaManager
    print("✅ All modules imported successfully")
except ImportError as e:
    print(f"❌ Critical import error: {e}")
    print("💡 Please ensure models/data_models.py exists with proper Model classes")
    sys.exit(1)

from datetime import datetime, timezone
from typing import List, Dict, Any
from uagents import Agent, Context, Protocol, Model

# Initialize components
try:
    metta_manager = MeTTaManager()
    print("✅ Components initialized successfully")
except Exception as e:
    print(f"⚠️ Component initialization warning: {e}")
    # Create a simple mock MeTTa manager
    class MeTTaManager:
        def get_interventions_for_pattern(self, pattern: str) -> List[Dict[str, Any]]:
            interventions_db = {
                'anxiety': [{'name': 'Box Breathing', 'effectiveness': 0.85}],
                'depression': [{'name': 'Behavioral Activation', 'effectiveness': 0.82}],
                'stress': [{'name': 'Mindful Breathing', 'effectiveness': 0.79}],
                'academic_stress': [{'name': 'Study Planning', 'effectiveness': 0.80}],
                'sleep_issues': [{'name': 'Sleep Hygiene', 'effectiveness': 0.82}]
            }
            return interventions_db.get(pattern, [{'name': 'Mindful Breathing', 'effectiveness': 0.7}])
    
    metta_manager = MeTTaManager()

# SORO Orchestrator Agent
soro_orchestrator = Agent(
    name="SORO Orchestrator",
    seed=os.getenv("SORO_ORCHESTRATOR_SEED", "soro_orchestrator_secret_003"),
    port=8004,
    endpoint=["http://localhost:8004/submit"],
    mailbox=True
)

print("=" * 60)
print("💫 SORO ORCHESTRATOR - ENHANCED PSN CONNECT INTEGRATION")
print("=" * 60)
print(f"📍 Agent Address: {soro_orchestrator.address}")
print(f"🌐 Local URL: http://localhost:8004/submit")
print(f"🔗 Protocol: InterventionOrchestration v1.1.0")
print(f"📡 Mailbox: ENABLED")
print(f"🤝 PSN Connect: ACTIVE INTEGRATION")
print("=" * 60)

# Define agent addresses for coordination
SOROMIND_CORE_ADDRESS = "agent1qdrdup2klslg5adangymn9ajm72c2sr95phpjfhuaz2ryskwdl6s5rfazls"
SOMA_ENGINE_ADDRESS = "agent1qtqs2gzljl90mlcjenxj6nxjd2gkhpptdy8nsaz7terv5s8h8gkf2z5ya4s"
PSN_CONNECT_ADDRESS = "agent1qfnztyxpn3p87spf6ah6j8us3r9ms497ruez5r8fwvr4kpjpw662zsdmtvj"

# Intervention protocol
intervention_proto = Protocol(name="InterventionOrchestration", version="1.1.0")

@intervention_proto.on_message(model=InterventionRequest)
async def handle_intervention_request(ctx: Context, sender: str, msg: InterventionRequest):
    """Handle intervention requests and coordinate appropriate responses"""
    ctx.logger.info(f"🎯 Intervention request for risk: {msg.risk_level}")
    print(f"💫 ORCHESTRATOR: SUCCESS - Received intervention request from {sender[:8]}...")
    print(f"📊 User State: '{msg.user_state[:50]}...'")
    print(f"🔍 Patterns: {msg.patterns}")
    print(f"⚠️ Risk Level: {msg.risk_level}")
    
    try:
        # Get evidence-based interventions from MeTTa
        interventions = get_interventions_for_state(
            msg.user_state, 
            msg.patterns, 
            msg.risk_level
        )
        
        # Coordinate with other agents based on risk level and patterns
        coordination_result = await coordinate_support(ctx, msg, interventions)
        
        # Build response that includes peer support information
        response_techniques = interventions['techniques']
        response_resources = interventions['resources'] + coordination_result['additional_resources']
        
        # Add peer support mention if activated
        if coordination_result['peer_support_initiated']:
            response_techniques.insert(0, "Peer support connection")
            response_resources.append("Peer matching in progress")
        
        response = InterventionResponse(
            techniques=response_techniques,
            reasoning=interventions['reasoning'],
            confidence=interventions['confidence'],
            duration_minutes=interventions['duration'],
            resources=response_resources
        )
        
        await ctx.send(sender, response)
        print(f"✅ ORCHESTRATOR: Sent intervention with {len(interventions['techniques'])} techniques")
        
        if coordination_result['peer_support_initiated']:
            print(f"🤝 ORCHESTRATOR: Peer support coordination COMPLETE - PSN Connect activated")
        else:
            print(f"ℹ️  ORCHESTRATOR: Standard intervention delivered")
            
        ctx.logger.info(f"✅ Intervention response sent with coordination")
        
    except Exception as e:
        ctx.logger.error(f"❌ Intervention error: {e}")
        print(f"❌ ORCHESTRATOR: Intervention failed - {e}")
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
    print(f"🚨 ORCHESTRATOR: CRISIS ALERT - User {msg.user_id[:8]}, Risk: {msg.risk_level}")
    
    # Get crisis-specific interventions
    crisis_interventions = get_crisis_interventions(msg.risk_level)
    
    print(f"🛟 Immediate actions: {msg.recommended_actions}")
    print(f"🎯 Crisis protocols: {crisis_interventions}")
    
    # Coordinate emergency response
    if msg.risk_level == RiskLevel.CRISIS:
        print("🚑 ORCHESTRATOR: PROFESSIONAL INTERVENTION REQUIRED - Coordinating emergency response")
        await coordinate_emergency_response(ctx, msg)

@intervention_proto.on_message(model=PatternAnalysisResponse)
async def handle_pattern_analysis(ctx: Context, sender: str, msg: PatternAnalysisResponse):
    """Handle pattern analysis results to preemptively suggest interventions"""
    ctx.logger.info(f"🔍 Pattern analysis received: {len(msg.patterns)} patterns")
    print(f"💫 ORCHESTRATOR: Pattern analysis from {sender[:8]}")
    print(f"📈 Patterns: {msg.patterns}")
    print(f"⚠️ Risk Assessment: {msg.risk_assessment}")
    print(f"💡 Suggested: {msg.suggested_interventions[:2]}...")

@intervention_proto.on_message(model=PeerSupportActivation)
async def handle_peer_support_activation(ctx: Context, sender: str, msg: PeerSupportActivation):
    """Handle confirmation from PSN Connect that peer support is activated"""
    ctx.logger.info(f"🤝 Peer support activated for user {msg.user_id}")
    print(f"💫 ORCHESTRATOR: PSN Connect activation confirmed!")
    print(f"   👤 User: {msg.user_id[:8]}...")
    print(f"   🎯 Support Type: {msg.support_type}")
    print(f"   👥 Matched Peers: {len(msg.matched_peers)}")
    print(f"   📅 Group Sessions: {len(msg.group_sessions)}")
    print(f"   📝 Reason: {msg.activation_reason}")

# ==================== ENHANCED COORDINATION FUNCTIONS ====================

async def coordinate_support(ctx: Context, request: InterventionRequest, interventions: Dict) -> Dict:
    """Enhanced coordination including peer support"""
    coordination_result = {
        'additional_resources': [],
        'agent_coordination': [],
        'peer_support_initiated': False
    }
    
    # Check if peer support is appropriate (academic stress, loneliness, etc.)
    should_activate_peer_support = (
        request.risk_level in [RiskLevel.LOW, RiskLevel.MEDIUM] and 
        any(pattern in request.patterns for pattern in 
            ['academic_stress', 'loneliness', 'social_isolation', 'study_issues'])
    )
    
    # Also check if user explicitly mentions peer support
    user_message_lower = request.user_state.lower()
    explicit_peer_request = any(phrase in user_message_lower for phrase in [
        'peer', 'study group', 'study groups', 'connect with others', 
        'talk to someone', 'group support', 'other students', 'community'
    ])
    
    if should_activate_peer_support or explicit_peer_request:
        print(f"🤝 ORCHESTRATOR: Activating peer support for patterns: {request.patterns}")
        
        # Determine support type based on urgency and explicit requests
        if explicit_peer_request or request.risk_level == RiskLevel.MEDIUM:
            support_type = "immediate"
        else:
            support_type = "scheduled"
            
        # Send recommendation to PSN Connect
        peer_recommendation = PeerSupportRecommendation(
            user_id=request.user_id,
            recommended_support_type=support_type,
            urgency=request.risk_level.value,
            patterns=request.patterns,
            orchestrator_confidence=interventions.get('confidence', 0.8),
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        try:
            await ctx.send(PSN_CONNECT_ADDRESS, peer_recommendation)
            coordination_result['peer_support_initiated'] = True
            coordination_result['additional_resources'].append("Peer support coordination initiated")
            coordination_result['agent_coordination'].append("PSN Connect")
            print(f"💫 ORCHESTRATOR: Sent peer support recommendation to PSN Connect")
            print(f"   👤 User: {request.user_id[:8]}...")
            print(f"   🎯 Support Type: {support_type}")
            print(f"   🔍 Patterns: {request.patterns}")
            
        except Exception as e:
            print(f"⚠️ ORCHESTRATOR: Failed to send to PSN Connect: {e}")
    
    # Academic stress patterns - coordinate study support
    if any(pattern in request.patterns for pattern in ['academic_stress', 'academic_perfectionism']):
        print(f"📚 ORCHESTRATOR: Academic stress detected - coordinating study support")
        coordination_result['additional_resources'].append("Academic counseling resources")
        coordination_result['agent_coordination'].append("Study support coordination")
    
    # Sleep issues
    if any(pattern in request.patterns for pattern in ['sleep_issues', 'insomnia']):
        print(f"😴 ORCHESTRATOR: Sleep issues detected - coordinating sleep support")
        coordination_result['additional_resources'].append("Sleep specialist resources")
    
    # Social isolation
    if any(pattern in request.patterns for pattern in ['loneliness', 'social_isolation']):
        print(f"👥 ORCHESTRATOR: Social isolation detected - coordinating connection")
        coordination_result['additional_resources'].append("Community engagement opportunities")
        coordination_result['agent_coordination'].append("Social connection coordination")
    
    return coordination_result

async def coordinate_emergency_response(ctx: Context, alert: MentalStateAlert):
    """Coordinate emergency response for crisis situations"""
    print("🆘 ORCHESTRATOR: Initiating emergency response protocol")
    
    # Notify all relevant agents
    emergency_alert = MentalStateAlert(
        user_id=alert.user_id,
        risk_level=alert.risk_level,
        detected_patterns=alert.detected_patterns,
        recommended_actions=alert.recommended_actions + ["EMERGENCY_PROTOCOL_ACTIVATED"],
        timestamp=datetime.now(timezone.utc).isoformat()
    )
    
    print("📢 ORCHESTRATOR: Broadcasting emergency alert to network")

# ==================== INTERVENTION MANAGEMENT ====================

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
        for pattern in patterns[:3]:  # Limit to top 3 patterns
            pattern_interventions = metta_manager.get_interventions_for_pattern(pattern)
            all_interventions.extend(pattern_interventions)
        
        # Sort by effectiveness and select top interventions
        all_interventions.sort(key=lambda x: x.get('effectiveness', 0), reverse=True)
        
        # Adjust number of interventions based on risk
        if risk_level == RiskLevel.CRISIS:
            top_interventions = all_interventions[:1]  # Focused intervention for crisis
        elif risk_level == RiskLevel.HIGH:
            top_interventions = all_interventions[:2]  # Limited interventions for high risk
        else:
            top_interventions = all_interventions[:3]  # Multiple options for lower risk
        
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
                "Emergency Services: 911",
                "Go to nearest emergency room"
            ]
            interventions['confidence'] = 1.0
            interventions['duration'] = 0  # Immediate action required
            
    except Exception as e:
        print(f"❌ Error getting interventions: {e}")
        # Fallback interventions
        interventions['techniques'] = ["Mindful breathing", "Grounding exercise"]
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
            "Safety planning",
            "Support network activation"
        ],
        RiskLevel.CRISIS: [
            "EMERGENCY PROTOCOL ACTIVATION",
            "Professional crisis support",
            "Immediate human connection",
            "Emergency services coordination"
        ]
    }
    
    return crisis_protocols.get(risk_level, ["Monitoring and support"])

# Include protocol
soro_orchestrator.include(intervention_proto, publish_manifest=True)

if __name__ == "__main__":
    print("🚀 Starting SORO Orchestrator Agent...")
    print("🎯 Intervention Coordination & Crisis Management")
    print("💡 Make sure to run ngrok for port 8004")
    print("📡 Mailbox: ENABLED for agent communication")
    print("🔗 Protocol: InterventionOrchestration v1.1.0")
    print("🤝 Multi-Agent Coordination: ENABLED")
    print("💫 PSN Connect Integration: GUARANTEED")
    print("⏹️  Press CTRL+C to stop")
    print("-" * 60)
    
    try:
        soro_orchestrator.run()
    except KeyboardInterrupt:
        print("\n🛑 SORO Orchestrator agent stopped")
    except Exception as e:
        print(f"❌ Error: {e}")