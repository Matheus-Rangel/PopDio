import os

POSTGRES = {
    'user': os.environ.get('POSTGRES_USER'),
    'pw': os.environ.get('POSTGRES_PASSWORD'),
    'db': os.environ.get('POSTGRES_DB'),
    'host': os.environ.get('POSTGRES_HOST'),
    'port': os.environ.get('POSTGRES_PORT'),
}
class Config():
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DATABASE_URI = ''

class DevelopmentConfig(Config):
    DEBUG = True
