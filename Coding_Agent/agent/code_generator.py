import requests
import re
from config import OLLAMA_API_URL

class CodeGenerator:
    def __init__(self):
        self.api_url = OLLAMA_API_URL

    def generate_code(self, prompt):
        enhanced_prompt = f"""
        Generate a Python function that calculates the Fibonacci sequence.
        Only return the function code, without any explanations or docstrings.
        The function should:
        - Be named 'fibonacci'
        - Take a single integer parameter 'n'
        - Return the nth number in the Fibonacci sequence
        - Use proper Python syntax and indentation
        """
        payload = {
            "model": "llama3",
            "prompt": enhanced_prompt,
            "stream": False
        }
        response = requests.post(self.api_url, json=payload)
        if response.status_code == 200:
            generated_code = response.json()['response']
            # Extract only the Python function from the response
            code_pattern = r'def fibonacci\(.*?(?=\n\n|\Z)'
            match = re.search(code_pattern, generated_code, re.DOTALL)
            if match:
                return match.group()
            else:
                raise ValueError("Failed to extract valid Python function from generated code")
        else:
            raise Exception(f"Failed to generate code: {response.text}")