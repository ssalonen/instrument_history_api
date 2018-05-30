"""
Production configuration used in docker
"""
from instrument_history_api.api_app.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', 'loota.verkkotiimi.fi', 'loota']

WARC_FOLDER = '/data'
DATABASES['default']['NAME'] = '/db/db.sqlite3'
STATIC_ROOT = '/app/static'

STATIC_URL = '/instrument_history_api/static/'

SECRET_KEY = os.environ['SECRET_KEY']