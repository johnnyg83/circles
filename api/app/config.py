import os
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Override this in production')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )
