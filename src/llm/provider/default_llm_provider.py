import base64
from typing import override
from src.llm.provider.llm_provider import LlmProvider
from src.llm.llm_prompt_contextualizer import LlmPromptContextualizer
from src.llm.service.llm_response_service import LlmResponseService


class DefaultLlmProvider(LlmProvider):
    def __init__(self, model: str, url: str, response_service: LlmResponseService):
        super().__init__(model, url, response_service)

    @override
    def get_message(self, image: base64) -> str:
        try:
            prompt = LlmPromptContextualizer.generate()
            return self.response_service.response(self.model, prompt, image)
        except Exception as e:
            return "An error occurred while processing the image. Please try again."
