from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str      # praksa je da env. varijable budu velikim slovima ali ce pydantic automatski konvertovati u velika slova
    database_port: str
    database_password: str  
    database_name: str 
    database_username: str

    class Config:
        env_file = '.env'

settings = Settings()