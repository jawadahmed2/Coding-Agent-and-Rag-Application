# tests/test_code_generator.py
import pytest
from agent.code_generator import CodeGenerator

def test_code_generator():
    generator = CodeGenerator()
    prompt = "Write a Python function that adds two numbers"
    generated_code = generator.generate_code(prompt)
    assert "def" in generated_code
    assert "return" in generated_code

