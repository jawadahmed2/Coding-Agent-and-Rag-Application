# agent/code_generator.py
import requests
from config import OLLAMA_API_URL

class CodeGenerator:
    def __init__(self):
        self.api_url = OLLAMA_API_URL

    def generate_code(self, prompt):
        payload = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(self.api_url, json=payload)
        if response.status_code == 200:
            return response.json()['response']
        else:
            raise Exception(f"Failed to generate code: {response.text}")