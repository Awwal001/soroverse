import os
from openai import OpenAI

class ASIClient:
    def __init__(self):
        api_key = os.getenv('ASI_API_KEY')
        self.client = OpenAI(api_key=api_key, base_url="https://api.asi1.ai/v1")
