from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

config_path = os.getenv("PROJECTS_CONFIG")

dotenv_path = f'{config_path}/financial_report_etl_project_config/.env'
load_dotenv(dotenv_path)

class Settings(BaseSettings):
    api_key: str = os.getenv("APY_KEY")

settings = Settings()


class DBSettings(BaseSettings):
    user_db: str = os.getenv("USER_DB")
    pw_db: str = os.getenv("PW_DB")
    cluster: str = os.getenv("CLUSTER")
    db_name: str = os.getenv("DB_NAME")

db_settings = DBSettings()


