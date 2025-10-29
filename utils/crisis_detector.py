import re
from typing import List, Dict, Any
from models.data_models import RiskLevel

class CrisisDetector:
    def __init__(self):
        self.crisis_keywords = [
            'suicide', 'kill myself', 'end my life', 'want to die',
            'better off dead', 'harm myself', 'self harm', 'cut myself',
            'cant take it', 'cant go on', 'end it all', 'no way out'
        ]
        
        self.high_risk_keywords = [
            'hopeless', 'helpless', 'worthless', 'burden',
            'alone forever', 'never get better', 'always sad'
        ]
        
        self.crisis_regex = re.compile(
            r'\b(suicide|kill myself|end my life|want to die|harm myself|self harm)\b',
            re.IGNORECASE
        )
    
    def detect_crisis_indicators(self, message: str) -> Dict[str, Any]:
        """Detect crisis indicators in user message"""
        message_lower = message.lower()
        
        # Check for immediate crisis keywords
        crisis_matches = list(self.crisis_regex.finditer(message_lower))
        crisis_words_found = [match.group() for match in crisis_matches]
        
        # Check for high-risk keywords
        high_risk_found = [word for word in self.high_risk_keywords if word in message_lower]
        
        # Assess risk level
        if crisis_words_found:
            risk_level = RiskLevel.CRISIS
        elif high_risk_found:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.LOW
        
        return {
            'risk_level': risk_level,
            'crisis_indicators': crisis_words_found,
            'high_risk_indicators': high_risk_found,
            'immediate_action_required': risk_level in [RiskLevel.CRISIS, RiskLevel.HIGH]
        }
    
    def get_crisis_response(self, risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Generate appropriate crisis response based on risk assessment"""
        risk_level = risk_assessment['risk_level']
        
        responses = {
            RiskLevel.LOW: {
                'message': "I'm here to listen and support you.",
                'actions': ['Continue conversation', 'Offer resources'],
                'escalation': False
            },
            RiskLevel.HIGH: {
                'message': "I'm concerned about what you're sharing. It sounds like you're going through a very difficult time. Please consider reaching out to professional support.",
                'actions': [
                    'Crisis Text Line: Text HOME to 741741',
                    'National Suicide Prevention Lifeline: 988',
                    'Offer to help connect with resources'
                ],
                'escalation': True
            },
            RiskLevel.CRISIS: {
                'message': "I'm very concerned about your safety. What you're describing sounds like an emergency situation. Please reach out for immediate help.",
                'actions': [
                    'Call 911 or go to the nearest emergency room',
                    'National Suicide Prevention Lifeline: 988 (available 24/7)',
                    'Crisis Text Line: Text HOME to 741741',
                    'Do not stay alone - reach out to someone you trust'
                ],
                'escalation': True,
                'emergency': True
            }
        }
        
        response = responses.get(risk_level, responses[RiskLevel.LOW])
        response['detected_indicators'] = risk_assessment['crisis_indicators'] + risk_assessment['high_risk_indicators']
        
        return response