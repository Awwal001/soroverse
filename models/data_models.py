from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
from uagents import Model

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRISIS = "crisis"

class MentalSupportRequest(Model):
    user_message: str
    emotion_context: Optional[str] = None
    session_id: str

class SupportResponse(Model):
    response_type: str
    message: str
    suggested_actions: List[str]
    risk_level: RiskLevel

class MentalStateAlert(Model):
    user_id: str
    risk_level: RiskLevel
    detected_patterns: List[str]
    timestamp: datetime
