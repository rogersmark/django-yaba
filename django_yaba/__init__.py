import os
from django.conf import settings

PROJECT_DIR = os.path.dirname(__file__)
if settings.MEDIA_ROOT is None:
    settings.MEDIA_ROOT = os.path.join(PROJECT_DIR, "media")

settings.TEMPLATE_DIRS += (
    os.path.join(PROJECT_DIR, "templates"),
    )
