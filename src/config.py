import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    token:str = os.getenv('TOKEN')
    id_telegram: str = os.getenv('ID_TELEGRAM')
    api_key: str = os.getenv('API_KEY')
