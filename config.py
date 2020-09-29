import os
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
email = os.getenv('EMAIL')
email_password = os.getenv('EMAIL_PASSWORD')


class Config(object):
    DEBUG = False
    TESTING = False
    SYSTEM_ROLES = ['user', 'administrator']
    NAME = 'ToDo REST API server'
    JWT_SECRET_KEY = 'your-secret-key'
    SECRET_KEY = 'your_secret_key'
    SECURITY_PASSWORD_SALT = 'your_security_password_salt'
    MAIL_DEFAULT_SENDER = email
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = email
    MAIL_PASSWORD = email_password
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class DevConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {'host': mongo_uri}
    NAME = 'ToDo REST API Development server'
