from enum import Enum


class LlmType(Enum):
    """
    Enum representing the different types of Language Model (LLM) providers supported.
    """
    OPENAI = "openai"
    # add more like this:
    # ANTHROPIC = "anthropic"
    # GOOGLE_VERTEX = "google_vertex"
