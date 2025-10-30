#!/usr/bin/env python3
"""
COMMON MODELS - Shared across all agents to ensure schema compatibility
"""

from typing import List, Dict, Any, Optional
from enum import Enum
from uagents import Model

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRISIS = "crisis"

# ==================== SOROMIND -> ORCHESTRATOR ====================

class InterventionRequest(Model):
    user_id: str
    user_state: str
    patterns: List[str]
    risk_level: RiskLevel
    timestamp: str
    preferences: Dict[str, Any] = {}
    session_context: Dict[str, Any] = {}

class InterventionResponse(Model):
    techniques: List[str]
    reasoning: str
    confidence: float
    duration_minutes: int
    resources: List[str]

# ==================== ORCHESTRATOR -> PSN CONNECT ====================

class PeerSupportRecommendation(Model):
    user_id: str
    recommended_support_type: str
    urgency: str
    patterns: List[str]
    orchestrator_confidence: float
    timestamp: str

# ==================== PSN CONNECT -> ORCHESTRATOR ====================

class PeerSupportActivation(Model):
    session_id: str
    user_id: str
    support_type: str
    matched_peers: List[Dict[str, Any]]
    group_sessions: List[Dict[str, Any]]
    activation_reason: str

# ==================== SOROMIND -> SOMA ENGINE ====================

class PatternAnalysisRequest(Model):
    user_message: str
    session_history: List[str] = []
    user_id: Optional[str] = None

class PatternAnalysisResponse(Model):
    user_id: Optional[str] = None
    patterns: List[str] = []
    emotions: List[str] = []
    risk_level: str = "low"
    enhanced_patterns: List[str] = []
    analysis_confidence: float = 0.0

# ==================== CRISIS ALERTS ====================

class MentalStateAlert(Model):
    user_id: str
    risk_level: str
    detected_patterns: List[str]
    recommended_actions: List[str]
    timestamp: str

# ==================== USER PREFERENCES ====================

class UserPreferences(Model):
    preferred_techniques: List[str] = []
    comfort_level: str = "beginner"
    time_availability: int = 15
    support_types: List[str] = []
    communication_style: str = "empathetic"