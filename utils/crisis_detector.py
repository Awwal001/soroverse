from models.data_models import RiskLevel

class CrisisDetector:
    def detect_crisis_indicators(self, message: str):
        message_lower = message.lower()
        crisis_words = ['suicide', 'kill myself', 'end my life']
        
        if any(word in message_lower for word in crisis_words):
            return {'risk_level': RiskLevel.CRISIS}
        return {'risk_level': RiskLevel.LOW}
