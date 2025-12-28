import json

import asyncio
import requests


class AIAssistant:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def answer(self, query) -> str:
        def _request():
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "user",
                        "content": f'Only respond "ja" or "nee": "{query}"',
                    }
                ],
            }
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=15,
            )
            return r.json()["choices"][0]["message"]["content"].replace(".", "")

        try:
            return await asyncio.to_thread(_request)
        except Exception:
            return "nee"
