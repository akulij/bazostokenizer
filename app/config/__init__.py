from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    online_sim_token: str
    db_path: str

settings = Settings()
