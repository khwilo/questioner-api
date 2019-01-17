'''Application configuration file'''
import os

class Config:
    """Parent configuration class"""
    DEBUG = False
    SECRET = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    DATABASE_CONNECTION_URL = os.getenv('DATABASE_CONNECTION_URL')

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
