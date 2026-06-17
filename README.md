# Math Assistant

A REST API that answers math questions in plain English using a local LLM and tool calling.

## How it works
A POST request with a plain English question is sent to the API. The LLM decides 
which math functions to call and in what order, your code executes them, and the 
results are sent back to the LLM which returns a final natural language answer.

## Setup
pip install ollama fastapi uvicorn pydantic
ollama pull qwen2.5:7b

## Usage
py -3.13 -m uvicorn main:app --reload

Open http://localhost:8000/docs to test via Swagger UI.

## Example
POST /calculate
{"payload": "what is 15 multiplied by 4, minus the square of 4?"}

{
  "result": "15 multiplied by 4 is 60. The square of 4 is 16. So, 60 minus 16 equals 44."
}

## Stack
Python · Ollama · FastAPI · Pydantic · qwen2.5:7b
