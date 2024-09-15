# agent/code_tester.py
import subprocess

class CodeTester:
    def test_code(self, code):
        # Write the code to a temporary file
        with open('temp_test.py', 'w') as f:
            f.write(code)

        # Run pytest on the temporary file
        result = subprocess.run(['pytest', 'temp_test.py'], capture_output=True, text=True)

        # Clean up the temporary file
        subprocess.run(['rm', 'temp_test.py'])

        return result.returncode == 0, result.stdout