import base64
from src.llm.llm_template import LlmTemplate


class LlmPromptContextualizer:
    @staticmethod
    def generate() -> str:
        return LlmTemplate.describe_image_prompt()
