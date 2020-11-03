import os


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
