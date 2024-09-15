import ast

class CodeTester:
    def test_code(self, code):
        # First, check if the code is valid Python syntax
        try:
            ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax error in generated code: {str(e)}"

        # If syntax is valid, write to file and run pytest
        with open('temp_test.py', 'w') as f:
            f.write(code)
            f.write("\n\n")
            f.write("""
def test_fibonacci():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(2) == 1
    assert fibonacci(3) == 2
    assert fibonacci(4) == 3
    assert fibonacci(5) == 5
    assert fibonacci(10) == 55
""")

        import pytest
        import io

        # Capture pytest output
        capture = io.StringIO()
        pytest.main(['temp_test.py'], capture_output=True, stream=capture)
        test_output = capture.getvalue()

        # Check if all tests passed
        if "failed" not in test_output and "error" not in test_output.lower():
            return True, "All tests passed"
        else:
            return False, test_output