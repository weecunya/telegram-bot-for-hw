import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    token:str = os.getenv('TOKEN')
    api_key: str = os.getenv('API_KEY')
