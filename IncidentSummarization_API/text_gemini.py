from vertexai.preview.generative_models import (
    GenerationConfig,
    GenerativeModel,
)
import vertexai
from dotenv import dotenv_values
# https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/prompts/examples/text_summarization.ipynb
# https://cloud.google.com/vertex-ai/docs/samples/aiplatform-sdk-summarization#aiplatform_sdk_summarization-python
def summarize_incident(text,config):
    """
    Take incident content to get summarization from gen-ai.
    Parameters:
    - text (str):  incident content from IT-incident-Case loaded to proper template.
    - config (int):  config values loaded from dotenv_values
    Returns:
    str: proper text to be fed to Generative AI to generate summarization.
    """
    
    PROJECT_ID = config["PROJECT_ID"]  # @param {type:"string"}
    GEN_AI_LOCATION= config["GEN_AI_LOCATION"]  # @param {type:"string"}
    vertexai.init(project=PROJECT_ID, location=GEN_AI_LOCATION)

    # Initialize Vertex AI client
    model = GenerativeModel("gemini-pro")
    
    # https://cloud.google.com/vertex-ai/docs/generative-ai/start/quickstarts/api-quickstart#try_chat_prompts
    responses = model.generate_content(text, stream=True)
    return responses
