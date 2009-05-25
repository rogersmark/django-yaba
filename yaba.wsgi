import os
import sys

sys.path.append('/home/f4nt/git-repos/personal/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_yaba.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

