import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    DYNAMO_TABLES = [
        {
            'TableName': 'users',
            'KeySchema': [dict(AttributeName='username', KeyType='HASH')],
            'AttributeDefinitions': [dict(AttributeName='username', AttributeType='S')],
            'ProvisionedThroughput': dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
        }, {
            'TableName': 'groups',
            'KeySchema': [dict(AttributeName='name', KeyType='HASH')],
            'AttributeDefinitions': [dict(AttributeName='name', AttributeType='S')],
            'ProvisionedThroughput': dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
        }
    ]


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True