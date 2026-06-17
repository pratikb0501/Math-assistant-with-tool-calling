from ollama import chat
from fastapi import FastAPI
from pydantic import BaseModel
from calculations import addition,subtraction,multiplication,square,available_functions

class RequestBody(BaseModel):
    payload:str

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/calculate")
def calculate(request:RequestBody):
    messages = [
        {'role': 'user', 'content': request.payload}
    ]
    response = chat(
        model='qwen2.5:7b',
        messages=messages,
        tools=available_functions.values()
    )
    messages.append(response.message)
    for tool_call in response.message.tool_calls or []:
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
    return {"result":final_response.message.content}
