import base64
from os import path
from src.llm.llm_type import LlmType
from src.llm.llm_provider_factory import LLMProviderFactory


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def main():
    image_path = path.join(path.dirname(path.realpath(__file__)), "../", "pen_example.jpeg")
    openai_llm = LLMProviderFactory.get_provider(LlmType.OPENAI)
    print(openai_llm.get_message(encode_image(image_path)))


if __name__ == "__main__":
    main()
