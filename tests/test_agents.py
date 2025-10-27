import pytest
from utils.crisis_detector import CrisisDetector

def test_crisis_detection():
    detector = CrisisDetector()
    result = detector.detect_crisis_indicators("I want to kill myself")
    assert result["risk_level"].value == "crisis"
