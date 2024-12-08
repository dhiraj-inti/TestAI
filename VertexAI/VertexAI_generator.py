import requests
from dotenv import load_dotenv
import os

load_dotenv()

VERTEXAI_API_KEY = os.getenv("VERTEXAI_API_KEY")
MODEL = "gemini-pro"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={VERTEXAI_API_KEY}"

def generate(query: str) -> str:

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": query
                    }
                ]
            }
        ]
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(URL, json=data, headers=headers)

    response = response.json()

    return response["candidates"][0]['content']['parts'][0]['text']