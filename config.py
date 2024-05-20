import logging
import os


class ConfigApp(object):
    # generic
    DEBUG = os.environ.get('DEBUG', True)
    TESTING = os.environ.get('TESTING', False)

    # security
    CSRF_ENABLED = os.environ.get('CSRF_ENABLED', False)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret')

    # sqlalchemy
    MYSQL_USER = os.environ.get('MYSQL_USER', 'qovoltis')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'qovoltis')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'test')
    SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_JWT_SECRET_KEY = "6d01b093e3a6746375b7bc87"


config = ConfigApp()