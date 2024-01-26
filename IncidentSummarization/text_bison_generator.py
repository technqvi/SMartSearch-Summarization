import vertexai
from vertexai.language_models import TextGenerationModel
#Error : https://codelabs.developers.google.com/text-summ-large-docs-stuffing?hl=en#4 

PROJECT_ID = "pongthorn"  # @param {type:"string"}
vertexai.init(project=PROJECT_ID, location="asia-southeast1")
generation_model = TextGenerationModel.from_pretrained("text-bison@002")
# https://cloud.google.com/vertex-ai/docs/generative-ai/start/quickstarts/api-quickstart#try_chat_prompts
parameters = {
    "temperature": 0.1,  # Temperature controls the degree of randomness in token selection.
    "max_output_tokens": 2048,  # Token limit determines the maximum amount of text output.
    # "top_p": 0.95,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
    #  "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    
}

# Define the prompt using the prompt template
response = generation_model.predict(text,**parameters,  
)

print(response )
output_file_path = "incident_summary.txt"
with open(output_file_path, 'w') as file:
    # Write the content to the file
    file.write(response)