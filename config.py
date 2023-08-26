import os
from dotenv import load_dotenv
from dotenv import dotenv_values

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ZalrM9dJAH3cxZ8UPbVD'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False