import os

import openai
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket

load_dotenv()

app = FastAPI()

openai_api_key = os.getenv("OPENAI_API_KEY")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        user_query = await websocket.receive_text()
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert cryptocurrency financial assistant.",
                },
                {"role": "user", "content": user_query},
            ],
            temperature=0.7,
            max_tokens=200,
        )
        ai_response = response["choices"][0]["message"]["content"]
        await websocket.send_text(ai_response)
