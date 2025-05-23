import os
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


class PostgresSettings(BaseModel):
    url: str = os.environ.get("POSTGRES_URL")
    echo: bool = os.environ.get("POSTGRES_ECHO").lower() == "true"


class MongoSettings(BaseModel):
    url: str = os.environ.get("MONGO_URL")


class Settings(BaseModel):
    api_prefix: str = os.environ.get("API_PREFIX")
    postgres: PostgresSettings = PostgresSettings()
    mongo: MongoSettings = MongoSettings()


settings = Settings()
