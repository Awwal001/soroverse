import os
from typing import List, Dict, Any
from hyperon import MeTTa
from models.data_models import RiskLevel

class MeTTaManager:
    def __init__(self):
        self.metta = MeTTa()
        self._initialize_knowledge_graph()
    
    def _initialize_knowledge_graph(self):
        """Initialize the mental health knowledge graph"""
        try:
            knowledge_path = os.path.join(os.path.dirname(__file__), 'mental_health.metta')
            with open(knowledge_path, 'r') as f:
                content = f.read()
                self.metta.run(content)
            print("✅ MeTTa knowledge graph initialized")
        except Exception as e:
            print(f"❌ Error: {e}")
