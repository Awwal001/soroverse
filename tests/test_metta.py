import pytest
from hyperon import MeTTa
from knowledge.metta_manager import MeTTaManager

class TestMeTTaIntegration:
    def setup_method(self):
        self.metta = MeTTa()
        self.manager = MeTTaManager()
    
    def test_basic_metta_operations(self):
        """Test basic MeTTa operations"""
        # Test adding atoms to space
        from hyperon import S, E
        atom = E(S("test"), S("atom"))
        self.metta.space().add_atom(atom)
        
        # Test querying
        results = self.metta.run('!(match &self (test atom) $x)')
        assert len(results) > 0
    
    def test_knowledge_graph_initialization(self):
        """Test that knowledge graph initializes properly"""
        # The manager should initialize without errors
        assert self.manager.metta is not None
        
        # Should be able to query basic patterns
        patterns = self.manager.query_emotional_patterns("anxiety")
        assert isinstance(patterns, list)
    
    def test_intervention_retrieval(self):
        """Test retrieval of interventions"""
        interventions = self.manager.get_interventions_for_pattern("perfectionism")
        assert isinstance(interventions, list)
        
        # Each intervention should have basic structure
        if interventions:
            intervention = interventions[0]
            assert 'name' in intervention
            assert 'effectiveness' in intervention
    
    def test_risk_assessment(self):
        """Test risk assessment functionality"""
        # Test low risk
        low_risk = self.manager.assess_crisis_risk("I'm doing okay", [])
        assert low_risk.value == "low"
        
        # Test crisis risk
        crisis_risk = self.manager.assess_crisis_risk("I want to kill myself", [])
        assert crisis_risk.value == "crisis"
    
    def test_crisis_protocols(self):
        """Test crisis protocol retrieval"""
        protocols = {
            "low": self.manager.get_crisis_protocol("low"),
            "medium": self.manager.get_crisis_protocol("medium"), 
            "high": self.manager.get_crisis_protocol("high"),
            "crisis": self.manager.get_crisis_protocol("crisis")
        }
        
        for level, protocol in protocols.items():
            assert protocol is not None
            assert 'actions' in protocol
            assert 'escalation' in protocol
            
            # Crisis level should have emergency flag
            if level == "crisis":
                assert protocol['emergency'] is True

if __name__ == "__main__":
    pytest.main([__file__, "-v"])