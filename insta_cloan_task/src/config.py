import os
from dotenv import load_dotenv


if os.getenv("ENV") in ["DEV", "TEST"]:

    load_dotenv(os.getenv("ENV_FILE", ".env"))
class Config:

    """database url"""
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
