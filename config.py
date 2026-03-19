# Flask Configuration Settings

class Config:
    SECRET_KEY = 'your_secret_key'
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'sqlite:///dev.db'

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'