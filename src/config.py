import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    token:str = os.getenv('TOKEN')
    id_telegram: int = int(os.getenv('ID_TELEGRAM'))
