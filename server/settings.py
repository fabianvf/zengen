import os

openai_api_key= os.getenv('OPENAI_API_KEY', "")
static_folder = os.getenv('STATIC_FOLDER', "../build/static")
database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///instance/koans.db")
