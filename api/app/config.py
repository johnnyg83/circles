import os
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Override this in production')
    #Test mongodb
    MONGODB_SETTINGS = {
        'db': 'circles',
        'host': 'mongodb+srv://circles.prroj.mongodb.net',
        'port': 27017,
        'username': 'admin',
        'password': 'admin_password'
    }