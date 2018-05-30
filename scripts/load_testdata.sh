#!/usr/bin/env bash
DJANGO_SETTINGS_MODULE=instrument_history_api.settings python manage.py shell -c "import sys; cmd=sys.stdin.read(); exec(cmd)" << 'EOF'
import os

import django
django.setup()

from instrument_history_api.warc_loader import process_warc_files

def iter_paths(root):
    paths = os.scandir(root)
    for entry in paths:
        if entry.is_file() and entry.name.endswith('.warc.gz'):
            yield entry

process_warc_files(*iter_paths('./testdata'))

EOF