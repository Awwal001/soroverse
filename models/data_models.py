#!/usr/bin/env python3
"""
Data Models for SOROverse Agents
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
from uagents import Model

# Risk Levels
class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRISIS = "crisis"

# Response Types
class ResponseType(str, Enum):
    REFLECTION = "reflection"
    INTERVENTION = "intervention"
    PEER_MATCH = "peer_match"
    ESCALATION = "escalation"

# Support Types
class SupportType(str, Enum):
    IMMEDIATE = "immediate"
    REFLECTION = "reflection"
    PEER = "peer"

# Support Request Types for PSN
class SupportRequestType(str, Enum):
    IMMEDIATE = "immediate"
    SCHEDULED = "scheduled"
    GROUP = "group"

# Core Mental Health Models
class MentalSupportRequest(Model):
    user_message: str
    emotion_context: Optional[str] = None
    support_type: Optional[SupportType] = None

class SupportResponse(Model):
    response_type: ResponseType
    message: str
    suggested_actions: List[str]
    follow_up_questions: List[str]

class MentalStateAlert(Model):
    user_id: str
    risk_level: RiskLevel
    detected_patterns: List[str]
    recommended_actions: List[str]
    timestamp: Optional[str] = None

# Pattern Analysis Models
class PatternAnalysisRequest(Model):
    user_message: str
    session_history: List[str]
    user_id: str

class PatternAnalysisResponse(Model):
    patterns: List[str]
    confidence: float
    risk_assessment: RiskLevel
    suggested_interventions: List[str]

# Intervention Models
class UserPreferences(Model):
    preferred_techniques: List[str] = []
    comfort_level: str = "beginner"
    time_availability: int = 15
    support_types: List[str] = ["self_help", "peer_support"]
    communication_style: str = "empathetic"

class InterventionRequest(Model):
    user_id: str
    user_state: str
    patterns: List[str]
    risk_level: RiskLevel
    timestamp: Optional[str] = None
    preferences: UserPreferences = None
    session_context: Optional[Dict[str, Any]] = None

class InterventionResponse(Model):
    techniques: List[str]
    reasoning: str
    confidence: float
    duration_minutes: int
    resources: List[str]

# Peer Support Network Models
class PeerSupportRequest(Model):
    request_id: str
    user_id: str
    current_state: str
    support_type: SupportRequestType
    availability: List[str]
    expertise_areas: List[str]
    urgency_level: str = "medium"
    preferences: Dict[str, Any] = {}

class PeerMatchResponse(Model):
    matched_peers: List[Dict[str, Any]]
    match_confidence: float
    group_sessions: List[Dict[str, Any]]
    recommended_approach: str
    estimated_wait_time: int

class SupportSession(Model):
    session_id: str
    user_id: str
    peer_id: str
    start_time: str
    status: str = "active"
    messages: List[Dict[str, str]] = []

class PeerSupportRecommendation(Model):
    user_id: str
    recommended_support_type: str
    urgency: str
    patterns: List[str]
    orchestrator_confidence: float
    timestamp: Optional[str] = None

class PeerSupportActivation(Model):
    session_id: str
    user_id: str
    support_type: str
    matched_peers: List[Dict[str, Any]]
    group_sessions: List[Dict[str, Any]]
    activation_reason: str

# Notification Models
class PeerMatchingNotification(Model):
    notification_type: str
    user_id: str
    details: Dict[str, Any]

class SessionStartNotification(Model):
    notification_type: str
    session_id: str
    user_id: str
    peer_id: str
    start_time: str

class SessionEndNotification(Model):
    notification_type: str
    session_id: str
    user_id: str
    peer_id: str
    end_time: str
    message_count: int
    status: str

# Chat Protocol Models
class PSNChatMessage(Model):
    message_id: str
    sender_id: str
    recipient_id: str
    content: str
    message_type: str = "text"
    timestamp: str
    session_id: Optional[str] = None

class PSNChatResponse(Model):
    response_id: str
    original_message_id: str
    content: str
    responder_id: str
    response_type: str = "support"
    timestamp: str