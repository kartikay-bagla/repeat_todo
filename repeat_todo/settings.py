import os

from dotenv import load_dotenv

load_dotenv(".env")

CWD = os.getcwd()

ENV = os.getenv("FLASK_ENV", default="production")
DEBUG = ENV == "development"
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", default="epic-secret-key")
