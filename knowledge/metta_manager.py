import os
from typing import List, Dict, Any, Optional
from hyperon import MeTTa, ValueAtom, S, E, V
from models.data_models import RiskLevel

class MeTTaManager:
    def __init__(self):
        self.metta = MeTTa()
        self._initialize_knowledge_graph()
    
    def _initialize_knowledge_graph(self):
        """Initialize the mental health knowledge graph"""
        try:
            # Load core mental health knowledge
            core_knowledge_path = os.path.join(os.path.dirname(__file__), 'mental_health.metta')
            interventions_path = os.path.join(os.path.dirname(__file__), 'interventions.metta')
            
            with open(core_knowledge_path, 'r') as f:
                core_content = f.read()
                self.metta.run(core_content)
            
            with open(interventions_path, 'r') as f:
                interventions_content = f.read()
                self.metta.run(interventions_content)
                
            print("✅ MeTTa knowledge graph initialized successfully")
            
        except Exception as e:
            print(f"❌ Error initializing MeTTa knowledge graph: {e}")
    
    def query_emotional_patterns(self, emotion: str) -> List[str]:
        """Query patterns associated with specific emotions"""
        try:
            query = f'!(match &self (association $pattern {emotion}) $pattern)'
            results = self.metta.run(query)
            
            patterns = []
            for result_group in results:
                for pattern_atom in result_group:
                    pattern_str = str(pattern_atom)
                    if pattern_str and not pattern_str.startswith('$'):
                        patterns.append(pattern_str)
            
            return list(set(patterns))  # Remove duplicates
            
        except Exception as e:
            print(f"Error querying emotional patterns: {e}")
            return []
    
    def get_interventions_for_pattern(self, pattern: str) -> List[Dict[str, Any]]:
        """Get interventions for specific cognitive patterns"""
        try:
            # Query for interventions that help with this pattern
            interventions = []
            
            # Check intervention effectiveness
            effectiveness_query = f'!(match &self (intervention_effectiveness ($intervention reduces {pattern} $effectiveness)) ($intervention $effectiveness))'
            effectiveness_results = self.metta.run(effectiveness_query)
            
            for result_group in effectiveness_results:
                if len(result_group) >= 2:
                    intervention = str(result_group[0])
                    effectiveness = float(str(result_group[1]))
                    
                    # Get intervention details
                    detail_query = f'!(match &self (intervention {intervention} ($key $value)) ($key $value))'
                    details = self.metta.run(detail_query)
                    
                    intervention_data = {
                        'name': intervention,
                        'effectiveness': effectiveness,
                        'details': {}
                    }
                    
                    for detail_group in details:
                        if len(detail_group) >= 2:
                            key = str(detail_group[0])
                            value = str(detail_group[1])
                            intervention_data['details'][key] = value
                    
                    interventions.append(intervention_data)
            
            return sorted(interventions, key=lambda x: x['effectiveness'], reverse=True)
            
        except Exception as e:
            print(f"Error getting interventions: {e}")
            return []
    
    def assess_crisis_risk(self, user_message: str, patterns: List[str]) -> RiskLevel:
        """Assess crisis risk based on message content and patterns"""
        try:
            risk_level = RiskLevel.LOW
            
            # Check for crisis indicators in message
            crisis_indicators = ['suicide', 'kill myself', 'end it all', 'harm myself', 
                               'cant go on', 'want to die', 'better off dead']
            
            message_lower = user_message.lower()
            crisis_words_found = [word for word in crisis_indicators if word in message_lower]
            
            if crisis_words_found:
                risk_level = RiskLevel.CRISIS
            elif any(pattern in ['catastrophizing', 'black_white_thinking'] for pattern in patterns):
                risk_level = RiskLevel.MEDIUM
            elif len(patterns) > 2:
                risk_level = RiskLevel.HIGH
            
            return risk_level
            
        except Exception as e:
            print(f"Error assessing crisis risk: {e}")
            return RiskLevel.MEDIUM  # Default to medium on error
    
    def get_crisis_protocol(self, risk_level: RiskLevel) -> Dict[str, Any]:
        """Get appropriate crisis response protocol"""
        protocols = {
            RiskLevel.LOW: {
                'actions': ['Continue monitoring', 'Provide resources'],
                'escalation': False
            },
            RiskLevel.MEDIUM: {
                'actions': ['Check in frequently', 'Offer immediate support', 'Suggest grounding techniques'],
                'escalation': False
            },
            RiskLevel.HIGH: {
                'actions': ['Immediate check-in', 'Crisis resources', 'Human connection'],
                'escalation': True
            },
            RiskLevel.CRISIS: {
                'actions': [
                    'National Suicide Prevention Lifeline: 988',
                    'Crisis Text Line: Text HOME to 741741',
                    'Immediate professional help',
                    'Do not leave person alone'
                ],
                'escalation': True,
                'emergency': True
            }
        }
        
        return protocols.get(risk_level, protocols[RiskLevel.MEDIUM])
    
    def add_user_pattern(self, user_id: str, pattern: str, emotion: str):
        """Add user-specific pattern to knowledge graph"""
        try:
            # Add user-specific association
            user_pattern = E(S("user_association"), S(user_id), S(pattern), S(emotion))
            self.metta.space().add_atom(user_pattern)
            
        except Exception as e:
            print(f"Error adding user pattern: {e}")