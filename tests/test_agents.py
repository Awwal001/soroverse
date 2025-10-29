import pytest
import asyncio
from unittest.mock import Mock, patch
from agents.soromind_core import process_user_message, UserSession
from knowledge.metta_manager import MeTTaManager
from utils.crisis_detector import CrisisDetector

class TestSoroMindCore:
    def setup_method(self):
        self.session = UserSession("test_session_001")
    
    @pytest.mark.asyncio
    async def test_process_normal_message(self):
        """Test processing of normal, non-crisis messages"""
        mock_ctx = Mock()
        
        response = await process_user_message(mock_ctx, "I'm feeling a bit stressed about work", self.session)
        
        assert response is not None
        assert len(response) > 0
        assert "stress" in response.lower() or "support" in response.lower()
    
    @pytest.mark.asyncio 
    async def test_process_crisis_message(self):
        """Test processing of crisis messages"""
        mock_ctx = Mock()
        
        response = await process_user_message(mock_ctx, "I want to kill myself", self.session)
        
        assert response is not None
        assert "988" in response or "crisis" in response.lower()
        assert self.session.risk_level.value in ["high", "crisis"]

class TestCrisisDetector:
    def setup_method(self):
        self.detector = CrisisDetector()
    
    def test_low_risk_detection(self):
        """Test detection of low-risk messages"""
        assessment = self.detector.detect_crisis_indicators("I'm feeling a bit sad today")
        assert assessment['risk_level'].value == "low"
        assert not assessment['immediate_action_required']
    
    def test_high_risk_detection(self):
        """Test detection of high-risk messages"""
        assessment = self.detector.detect_crisis_indicators("I feel hopeless and can't go on")
        assert assessment['risk_level'].value in ["high", "crisis"]
        assert assessment['immediate_action_required']
    
    def test_crisis_response_generation(self):
        """Test crisis response generation"""
        assessment = self.detector.detect_crisis_indicators("I want to end my life")
        response = self.detector.get_crisis_response(assessment)
        
        assert response['escalation'] is True
        assert len(response['actions']) > 0
        assert any('988' in action for action in response['actions'])

class TestMeTTaManager:
    def setup_method(self):
        self.metta_manager = MeTTaManager()
    
    def test_pattern_query(self):
        """Test querying emotional patterns"""
        patterns = self.metta_manager.query_emotional_patterns("anxiety")
        assert isinstance(patterns, list)
    
    def test_crisis_risk_assessment(self):
        """Test crisis risk assessment"""
        risk_level = self.metta_manager.assess_crisis_risk("I'm feeling okay", [])
        assert risk_level.value in ["low", "medium", "high", "crisis"]
    
    def test_crisis_protocol(self):
        """Test crisis protocol retrieval"""
        protocol = self.metta_manager.get_crisis_protocol("crisis")
        assert protocol is not None
        assert 'actions' in protocol
        assert isinstance(protocol['actions'], list)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])