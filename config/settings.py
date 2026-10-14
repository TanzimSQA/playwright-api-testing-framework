import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    BASE_URL: str = os.getenv("BASE_URL", "https://dummyjson.com").rstrip("/")
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "15000"))
    MAX_RESPONSE_TIME_MS: float = float(os.getenv("MAX_RESPONSE_TIME_MS", "1500"))
    
    # Auth test credentials
    AUTH_USERNAME: str = os.getenv("AUTH_USERNAME", "emilys")
    AUTH_PASSWORD: str = os.getenv("AUTH_PASSWORD", "emilyspass")
    
    # Common headers
    DEFAULT_HEADERS: dict = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Playwright-API-Testing-Framework/1.0 (Python/Playwright)",
    }
    
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
