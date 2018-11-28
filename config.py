import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    # Figure out what this is:
    SQLALCHEMY_DATABASE_URI = 'mysql://scott:tiger@localhost/mydatabase'

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/test.db'


class TestingConfig(Config):
    TESTING = True