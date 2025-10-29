from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
from uuid import UUID, uuid4
from uagents import Model

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRISIS = "crisis"

class SupportType(str, Enum):
    IMMEDIATE = "immediate"
    REFLECTION = "reflection"
    PEER = "peer"
    CRISIS = "crisis"

class ResponseType(str, Enum):
    REFLECTION = "reflection"
    INTERVENTION = "intervention"
    PEER_MATCH = "peer_match"
    ESCALATION = "escalation"

# Input/Output Models for Chat Protocol
class MentalSupportRequest(Model):
    user_message: str
    emotion_context: Optional[str] = None
    support_type: Optional[SupportType] = None
    session_id: str

class SupportResponse(Model):
    response_type: ResponseType
    message: str
    suggested_actions: List[str]
    follow_up_questions: List[str]
    risk_level: RiskLevel
    session_id: str

# Internal Agent Communication Models
class MentalStateAlert(Model):
    user_id: str
    risk_level: RiskLevel
    detected_patterns: List[str]
    recommended_actions: List[str]
    timestamp: datetime

class PatternAnalysisRequest(Model):
    user_message: str
    session_history: List[str]
    current_emotion: Optional[str] = None

class PatternAnalysisResponse(Model):
    patterns: List[str]
    confidence: float
    risk_assessment: RiskLevel
    suggested_interventions: List[str]

class PeerMatchRequest(Model):
    user_id: str
    current_state: str
    preferred_support_type: SupportType
    availability: List[str]
    expertise_areas: List[str]

class PeerMatchResponse(Model):
    matched_peers: List[Dict[str, Any]]
    match_confidence: float
    group_sessions: List[Dict[str, Any]]

class InterventionRequest(Model):
    user_state: str
    patterns: List[str]
    risk_level: RiskLevel
    preferences: Dict[str, Any]

class InterventionResponse(Model):
    techniques: List[str]
    reasoning: str
    confidence: float
    duration_minutes: int
    resources: List[str]