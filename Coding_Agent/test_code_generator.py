from agent.code_generator import CodeGenerator

generator = CodeGenerator()
prompt = "Write a Python function that adds two numbers"
generated_code = generator.generate_code(prompt)

print(generated_code)

######## Here is the response from ollama Llama3 local llm #####
"""
Here is a simple Python function that adds two numbers:
```
def add_numbers(a, b):
    return a + b
```
You can call this function with two arguments to get the result of their addition. For example:
```
result = add_numbers(2, 3)
print(result)  # Output: 5
```
Note that this function takes two arguments `a` and `b`, and returns their sum using the built-in `+` operator.

If you want to make it more robust, you could also handle cases where one or both of the inputs are not numbers (e.g. strings, lists, etc.). For example:
```
def add_numbers(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers")
    return a + b
```
"""