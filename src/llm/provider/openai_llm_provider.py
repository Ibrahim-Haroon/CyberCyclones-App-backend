from src.util.env import Env
from src.llm.provider.default_llm_provider import DefaultLlmProvider
from src.llm.service.openai_llm_response_service import OpenAiLlmResponseService


class OpenAiLlmProvider(DefaultLlmProvider):
    def __init__(self):
        self.model = "gpt-4o-mini"
        self.url = "https://api.openai.com/v1/chat/completions"
        self.__api_key = Env()["OPENAI_API_KEY"]
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.__api_key}",
        }
        self.response_service = OpenAiLlmResponseService(self.model, self.url, self.headers)

        super().__init__(self.model, self.url, self.response_service)
