import os

from sqlalchemy.engine.url import URL

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

ADMINS = frozenset(['email@rosgvard.ru'])
SECRET_KEY = 'somekey'

# SQLALCHEMY_DATABASE_URI = URL(**db_url)
DATABASE_CONNECT_OPTIONS = {}
THREADS_PER_PAGE = 4