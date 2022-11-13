import os

from dotenv import load_dotenv

app_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class Config:
    SECRET_KEY = 'CHANGEME'
    DEBUG = True
    DB_ENGINE = os.getenv('DB_ENGINE', default='postgresql')
    DB_NAME = os.getenv('DB_NAME', default='postgres')
    DB_USER = os.getenv('DB_USER', default='postgres')
    DB_PASS = os.getenv('DB_PASS', default='postgres')
    DB_HOST = os.getenv('DB_HOST', default='db')
    # SQLALCHEMY_DATABASE_URI = f'{DB_ENGINE}://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app_dir, 'app.db')
