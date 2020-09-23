import os
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")


class Config(object):
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = mongo_uri
