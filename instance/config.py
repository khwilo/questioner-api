'''Application configuration file'''
import os

class Config(object):
    """Parent configuration class"""
    DEBUG = False
    SECRET = os.getenv('SECRET_KEY')

class DevelopmentConfig(Config):
    """Development environment configurations"""
    DEBUG = True

class TestingConfig(Config):
    """Testing environment configurations"""
    TESTING = True
    DEBUG = True

class StagingConfig(Config):
    """Staging environment configurations"""
    DEBUG = True

class ProductionConfig(Config):
    """Production environment configurations"""
    DEBUG = False
    TESTING = False

APP_CONFIG = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
