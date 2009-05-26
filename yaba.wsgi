import os
import sys

sys.path.append('%s/../' % os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_yaba.settings'
os.environ['PYTHON_EGG_CACHE'] = "%s/cache" % os.path.dirname(__file__)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

