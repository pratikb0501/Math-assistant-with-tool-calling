from ollama import chat

def addition(a: int, b: int) -> int: 
    """
    Add two numbers
    Args:
        a: First number
        b: Second number
    Returns:
        int: Sum of the two numbers
    """
    return a + b

def subtraction(a: int, b: int) -> int:
    """
    Subtract two numbers
    Args:
        a: First number
        b: Second number
    Returns:
        int: Subtract of the two numbers
    """
    return a - b

def multiplication(a: int, b: int) -> int:
    """
    Multiply two numbers
    Args:
        a: First number
        b: Second number
    Returns:
        int: Multiplication of the two numbers
    """
    return a * b

def square(a:int)->int:
    """
    Sqaure of a number
    Args:
        a: First number
    Returns:
        int: Square of a number
    """
    return a*a



available_functions = {
    'addition': addition,
    'subtraction': subtraction,
    'multiplication': multiplication,
    'square': square,
}

messages = [
    {'role': 'user', 'content': 'what is 15 multiplied by 3, minus the square of 4?'}
]

response = chat(
    model='qwen2.5:7b',
    messages=messages,
    tools=available_functions.values()
    # stream=True,
)

messages.append(response.message)
for tool_call in response.message.tool_calls:
    function_name = tool_call.function.name
    arguments = tool_call.function.arguments
    function_to_call = available_functions[function_name]
    result = function_to_call(**arguments)
    print(f"Called {function_name}({arguments}) = {result}")
    messages.append({
        'role': 'tool',
        'content': str(result),
    })

final_response = chat(
    model='qwen2.5:7b',
    messages=messages,
)

print("\nFinal answer:", final_response.message.content)