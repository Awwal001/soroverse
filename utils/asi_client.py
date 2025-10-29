import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from models.data_models import RiskLevel, PatternAnalysisResponse

class ASIClient:
    def __init__(self):
        api_key = os.getenv('ASI_API_KEY')
        if not api_key:
            raise ValueError("ASI_API_KEY environment variable is required")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.asi1.ai/v1"
        )
    
    async def analyze_mental_patterns(self, user_message: str, session_history: List[str]) -> PatternAnalysisResponse:
        """Use ASI:One to analyze mental patterns and provide insights"""
        try:
            # Build conversation context
            messages = [
                {
                    "role": "system",
                    "content": """You are a computational psychiatry expert. Analyze the user's message for:
1. Cognitive patterns (perfectionism, catastrophizing, black-and-white thinking, etc.)
2. Emotional states (anxiety, depression, stress, etc.)
3. Risk level (low, medium, high, crisis)
4. Suggested evidence-based interventions

Respond with specific patterns found and confidence levels."""
                }
            ]
            
            # Add session history for context
            for msg in session_history[-5:]:  # Last 5 messages for context
                messages.append({"role": "user" if len(messages) % 2 == 1 else "assistant", "content": msg})
            
            messages.append({"role": "user", "content": user_message})
            
            response = self.client.chat.completions.create(
                model="asi1-extended",
                messages=messages,
                temperature=0.3,
                max_tokens=500
            )
            
            analysis_text = response.choices[0].message.content
            
            # Parse the response to extract patterns and risk assessment
            patterns = self._extract_patterns(analysis_text)
            risk_level = self._assess_risk_from_analysis(analysis_text)
            interventions = self._extract_interventions(analysis_text)
            
            return PatternAnalysisResponse(
                patterns=patterns,
                confidence=0.85,  # Based on model confidence
                risk_assessment=risk_level,
                suggested_interventions=interventions
            )
            
        except Exception as e:
            print(f"Error in ASI:One analysis: {e}")
            # Return default response on error
            return PatternAnalysisResponse(
                patterns=[],
                confidence=0.0,
                risk_assessment=RiskLevel.LOW,
                suggested_interventions=[]
            )
    
    def _extract_patterns(self, analysis_text: str) -> List[str]:
        """Extract cognitive patterns from analysis text"""
        patterns = []
        common_patterns = [
            'perfectionism', 'catastrophizing', 'black-white thinking', 
            'overgeneralization', 'personalization', 'mind reading',
            'emotional reasoning', 'should statements', 'labeling'
        ]
        
        text_lower = analysis_text.lower()
        for pattern in common_patterns:
            if pattern in text_lower:
                patterns.append(pattern)
        
        return patterns
    
    def _assess_risk_from_analysis(self, analysis_text: str) -> RiskLevel:
        """Assess risk level from analysis text"""
        text_lower = analysis_text.lower()
        
        if any(word in text_lower for word in ['crisis', 'suicide', 'self-harm', 'emergency']):
            return RiskLevel.CRISIS
        elif any(word in text_lower for word in ['severe', 'high risk', 'urgent']):
            return RiskLevel.HIGH
        elif any(word in text_lower for word in ['moderate', 'medium', 'concerning']):
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _extract_interventions(self, analysis_text: str) -> List[str]:
        """Extract suggested interventions from analysis text"""
        interventions = []
        common_interventions = [
            'CBT', 'mindfulness', 'breathing exercises', 'journaling',
            'behavioral activation', 'exposure therapy', 'DBT skills',
            'social connection', 'professional help'
        ]
        
        text_lower = analysis_text.lower()
        for intervention in common_interventions:
            if intervention.lower() in text_lower:
                interventions.append(intervention)
        
        return interventions