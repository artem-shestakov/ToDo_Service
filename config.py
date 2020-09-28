import os
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")


class Config(object):
    DEBUG = False
    TESTING = False
    SYSTEM_ROLES = ['user', 'administrator']
    NAME = 'ToDo REST API server'
    JWT_SECRET_KEY = 'your-secret-key'
    SECRET_KEY = 'your_secret_key'
    SECURITY_PASSWORD_SALT = 'your_security_password_salt'


class DevConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {'host': mongo_uri}
    NAME = 'ToDo REST API Development server'
