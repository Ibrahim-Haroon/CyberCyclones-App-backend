import base64
from abc import ABC, abstractmethod
from src.llm.service.llm_response_service import LlmResponseService


class LlmProvider(ABC):
    def __init__(self, model: str, url: str, response_service: LlmResponseService):
        """
        :param model: The model identifier used by this LLM provider. (ex. "gpt-3.5-turbo")
        :param url: The URL for the LLM API.
        :param response_service: The instance of a class that implements the LlmResponseService interface
        """
        self.model = model
        self.url = url
        self.response_service = response_service

    @abstractmethod
    def get_message(self, image: base64) -> str:
        """
        This method is used to get a message from the LLM provider

        :param image: The image to classify
        :return: The response from the LLM provider
        :rtype: str
        """
        pass
