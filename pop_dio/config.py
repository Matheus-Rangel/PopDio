import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class ProductionCOnfig(Config):
    DATABASE_URI = ''

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
