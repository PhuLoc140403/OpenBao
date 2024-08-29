import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    BAO_ADDR = os.getenv("BAO_ADDR", "http://127.0.0.1:8200")
    BAO_TOKEN = os.getenv("BAO_TOKEN", "s.vBZzrwXBqW0MpdJ1Oh57gKhK")
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "postgresql://openbao_user:password@localhost/openbao_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = Config()
