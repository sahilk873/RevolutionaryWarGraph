from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


# File paths
INPUT_FILE_PATH = 'revolution.txt'
ENTITIES_OUTPUT_FILE = 'structured_entities_output_new.json'
RELATIONSHIPS_OUTPUT_FILE = 'structured_relationships_output_new.json'

# OpenAI model configuration
OPENAI_MODEL = "gpt-4o-2024-08-06"  # Ensure this model supports Structured Outputs

INDEX_NAME = 'relationships-index'
EMBEDDING_DIMENSION = 1536  # Adjust based on your embedding size

# Other configurations can be added here
