import base64
from abc import ABC, abstractmethod


class LlmResponseService(ABC):
    @abstractmethod
    def response(self, role: str, prompt: str, image: base64) -> str:
        """
        This method is used to as a baseline behavior for all LLM Response Services

        :param role: The behavior/persona for the model to inherit
        :param prompt: The task for the model to complete
        :param image: The image to classify
        :return: response from LLM
        :rtype: str
        """
        pass
