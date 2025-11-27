import os
from src.config.dev_config import DevConfig
from src.config.production import ProductionConfig

basedir = os.path.abspath(os.path.dirname(__file__))
db_filename = 'instance/' + os.getenv('DB_NAME', 'blog.db')


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, db_filename)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    def __init__(self):
        self.dev_config = DevConfig()
        self.production_config = ProductionConfig()