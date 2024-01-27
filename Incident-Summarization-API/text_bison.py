import vertexai
from vertexai.language_models import TextGenerationModel
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

    # Initialize Vertex AI client
    vertexai.init(project=PROJECT_ID, location=GEN_AI_LOCATION)
    generation_model = TextGenerationModel.from_pretrained("text-bison@002")
    
    # https://cloud.google.com/vertex-ai/docs/generative-ai/start/quickstarts/api-quickstart#try_chat_prompts
    parameters = {
        "temperature": 0.5,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 2048,  # Token limit determines the maximum amount of text output.
        # "top_p": 0.95,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        #  "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
        
    }
    # Define the prompt using the prompt template
    response = generation_model.predict(text,**parameters,  
    ).text

    return response

