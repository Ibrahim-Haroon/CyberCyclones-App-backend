import base64
import requests
from typing import override
from src.llm.service.llm_response_service import LlmResponseService


class OpenAiLlmResponseService(LlmResponseService):
    def __init__(self, model: str, endpoint: str, headers: dict):
        self.model = model
        self.endpoint = endpoint
        self.headers = headers

    @override
    def response(self, role: str, prompt: str, image: base64) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": role
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image}"
                            },
                        },
                    ],
                }
            ]
        }

        response = requests.post(
            url=self.endpoint,
            headers=self.headers,
            json=payload
        )

        response_data = response.json()
        try:
            return response_data["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            raise ValueError("No content found in the response")
