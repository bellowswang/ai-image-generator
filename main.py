# imports
import openai  # OpenAI Python library to make API calls
from config import api_key

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

openai.api_key = api_key

def call_dalle_api(prompt):
    # call the OpenAI API
    generation_response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512",
        response_format="url",
    )
    url = generation_response['data'][0]['url']
    print(url)
    return url

app = FastAPI()

origins = [
    "http://localhost:3000/create",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

@app.post("/dalle/")
async def dalle(payload: Message):
    messages = payload.message
    return call_dalle_api(messages)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='localhost', port=8080)