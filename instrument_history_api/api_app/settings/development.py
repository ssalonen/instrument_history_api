"""
Development configuration used for testing and developing
"""
from instrument_history_api.api_app.settings.base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

SECRET_KEY = '5-zl#+uom!ysv6-ot914h3$o)079h5#e^+9tr(t#2@1qx52gfn'

WARC_FOLDER = '/home/salski/src/warc-testdata'
DATABASES['default']['NAME'] = os.path.join(BASE_DIR, '/db.sqlite3')

STATIC_ROOT = '/tmp/instrument_history_api-static'