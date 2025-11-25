import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_filename = 'instance/' +  os.getenv('DB_NAME', 'blog.db')

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, db_filename)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
