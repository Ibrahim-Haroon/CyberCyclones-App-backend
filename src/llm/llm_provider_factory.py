from src.llm.llm_type import LlmType
from src.util.singleton import singleton
from src.llm.provider.llm_provider import LlmProvider


@singleton
class LLMProviderFactory:
    @staticmethod
    def get_provider(llm: LlmType) -> LlmProvider:
        match llm:
            case LlmType.OPENAI:
                from src.llm.provider.openai_llm_provider import OpenAiLlmProvider
                return OpenAiLlmProvider()
            case _:
                raise ValueError(f"Unsupported LLM provider: {llm}")
