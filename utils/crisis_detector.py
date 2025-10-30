import re
from typing import List, Dict, Any
from models.data_models import RiskLevel

class CrisisDetector:
    def __init__(self):
        # EXPANDED crisis keywords - include variations
        self.crisis_keywords = [
            'suicide', 'kill myself', 'end my life', 'want to die',
            'better off dead', 'harm myself', 'self harm', 'cut myself',
            'cant take it', 'cant go on', 'end it all', 'no way out',
            'feel like killing myself', 'want to kill myself', 'thinking of suicide',
            'planning suicide', 'suicidal', 'end everything', 'give up on life',
            'not want to live', 'tired of living', 'life is pointless'
        ]
        
        self.high_risk_keywords = [
            'hopeless', 'helpless', 'worthless', 'burden',
            'alone forever', 'never get better', 'always sad',
            'empty inside', 'nothing matters', 'can\'t cope',
            'overwhelming pain', 'unbearable', 'no future'
        ]
        
        # IMPROVED regex pattern - more comprehensive
        crisis_patterns = [
            r'\b(suicide|suicidal)\b',
            r'\b(kill\s+(my)?self)\b',
            r'\b(end\s+(my\s+)?life)\b',
            r'\b(want\s+to\s+die)\b',
            r'\b(better\s+off\s+dead)\b',
            r'\b(harm\s+(my)?self)\b',
            r'\b(self\s+harm)\b',
            r'\b(cut\s+(my)?self)\b',
            r'\b(end\s+it\s+all)\b',
            r'\b(no\s+way\s+out)\b',
            r'\b(feel\s+like\s+kill)\b',
            r'\b(not\s+want\s+to\s+live)\b',
            r'\b(tired\s+of\s+living)\b',
            r'\b(life\s+is\s+pointless)\b'
        ]
        
        self.crisis_regex = re.compile(
            '|'.join(crisis_patterns),
            re.IGNORECASE
        )
        
        print("✅ Crisis Detector initialized with expanded patterns")
    
    def detect_crisis_indicators(self, message: str) -> Dict[str, Any]:
        """Detect crisis indicators in user message"""
        message_lower = message.lower().strip()
        
        print(f"🔍 Analyzing message: '{message_lower}'")  # DEBUG
        
        # Check for immediate crisis keywords using regex
        crisis_matches = list(self.crisis_regex.finditer(message_lower))
        crisis_words_found = [match.group() for match in crisis_matches]
        
        # Also check using simple string matching as backup
        simple_crisis_matches = [word for word in self.crisis_keywords if word in message_lower]
        crisis_words_found.extend(simple_crisis_matches)
        crisis_words_found = list(set(crisis_words_found))  # Remove duplicates
        
        # Check for high-risk keywords
        high_risk_found = [word for word in self.high_risk_keywords if word in message_lower]
        
        print(f"🔍 Crisis matches: {crisis_words_found}")  # DEBUG
        print(f"🔍 High risk matches: {high_risk_found}")  # DEBUG
        
        # Assess risk level
        if crisis_words_found:
            risk_level = RiskLevel.CRISIS
            print(f"🚨 CRISIS DETECTED: {crisis_words_found}")  # DEBUG
        elif high_risk_found:
            risk_level = RiskLevel.HIGH
            print(f"⚠️ HIGH RISK DETECTED: {high_risk_found}")  # DEBUG
        else:
            risk_level = RiskLevel.LOW
            print("✅ No crisis detected")  # DEBUG
        
        return {
            'risk_level': risk_level,
            'crisis_indicators': crisis_words_found,
            'high_risk_indicators': high_risk_found,
            'immediate_action_required': risk_level in [RiskLevel.CRISIS, RiskLevel.HIGH]
        }
    
    def get_crisis_response(self, risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Generate appropriate crisis response based on risk assessment"""
        risk_level = risk_assessment['risk_level']
        
        print(f"🎯 Generating crisis response for level: {risk_level}")  # DEBUG
        
        responses = {
            RiskLevel.LOW: {
                'message': "I'm here to listen and support you through whatever you're experiencing.",
                'actions': ['Continue conversation', 'Offer coping strategies'],
                'escalation': False
            },
            RiskLevel.HIGH: {
                'message': "I'm deeply concerned about what you're sharing. It sounds like you're in tremendous pain right now. Please know that professional support is available and can help.",
                'actions': [
                    'Crisis Text Line: Text HOME to 741741',
                    'National Suicide Prevention Lifeline: 988',
                    'International crisis resources available',
                    'Reach out to someone you trust immediately'
                ],
                'escalation': True
            },
            RiskLevel.CRISIS: {
                'message': "🚨 **I'm very concerned about your immediate safety.** What you're describing sounds like a life-threatening emergency. Your life is precious and worth protecting.",
                'actions': [
                    '**Call 911 or your local emergency number RIGHT NOW**',
                    'National Suicide Prevention Lifeline: 988 (available 24/7)',
                    'Crisis Text Line: Text HOME to 741741',
                    'Go to the nearest hospital emergency room',
                    '**Do not stay alone** - reach out to someone you trust immediately',
                    'International Association for Suicide Prevention resources'
                ],
                'escalation': True,
                'emergency': True
            }
        }
        
        response = responses.get(risk_level, responses[RiskLevel.LOW])
        response['detected_indicators'] = risk_assessment['crisis_indicators'] + risk_assessment['high_risk_indicators']
        
        print(f"📝 Crisis response prepared: {response['message'][:100]}...")  # DEBUG
        
        return response