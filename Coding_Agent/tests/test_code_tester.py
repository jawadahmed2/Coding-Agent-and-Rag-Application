# tests/test_code_tester.py
import pytest
from agent.code_tester import CodeTester

def test_code_tester():
    tester = CodeTester()
    valid_code = """
def test_addition():
    assert 1 + 1 == 2
"""
    is_valid, output = tester.test_code(valid_code)
    assert is_valid

    invalid_code = """
def test_addition():
    assert 1 + 1 == 3
"""
    is_valid, output = tester.test_code(invalid_code)
    assert not is_valid