from ollama import chat
from fastapi import FastAPI, HTTPException
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
    try:
        messages = [
            {'role': 'system', 'content': 'You are a math assistant. Give short, direct answers. No LaTeX formatting.'},
            {'role': 'user', 'content': request.payload}
        ]
        response = chat(
            model='qwen2.5:7b',
            messages=messages,
            tools=available_functions.values()
        )
        if not response.message.tool_calls:
            raise HTTPException(status_code=400, detail="I can only answer math questions.")
        messages.append(response.message)
        for tool_call in response.message.tool_calls:
            function_name = tool_call.function.name
            if function_name not in available_functions:
                raise HTTPException(status_code=400, detail=f"Unknown tool requested: {function_name}")
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

