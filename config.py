import os
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")


class Config(object):
    DEBUG = False
    TESTING = False
    NAME = 'ToDo REST API server'


class DevConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {'host': mongo_uri}
    NAME = 'ToDo REST API Development server'
