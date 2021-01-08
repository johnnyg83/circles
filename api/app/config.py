import os
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Override this in production')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
