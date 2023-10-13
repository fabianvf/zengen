import os

openai_api_key= os.getenv('OPENAI_API_KEY', "")
static_folder = os.getenv('STATIC_FOLDER', "../build")
