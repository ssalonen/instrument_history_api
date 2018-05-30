"""
WSGI config for instrument_history_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import logging.config

logging_ini = os.environ.get('LOGGING_INI', None)
if logging_ini:
    logging.config.fileConfig(os.environ['LOGGING_INI'])

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "not_set")

application = get_wsgi_application()
