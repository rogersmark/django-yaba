# Django settings for django_yaba project.
import os

###############################################
# django-yaba specific settings below         #
###############################################
# GitHub UserName for sidebar GitHub List - Leave blank if you don't want to use it
GITHUB_USERNAME = 'f4nt'

# Twitter UserName for sidebar Twitter List and Automatic Tweets
TWITTER_USERNAME = 'f4nt'
TWITTER_PASSWORD = "getyourownplzk?"

# Blog Name
BLOG_NAME = '..::f4ntasmic studios::..'

# Blog URL
ROOT_BLOG_URL = 'http://testblog/'

# Root system path
PROJECT_DIR = os.path.dirname(__file__)

# Recaptcha keys
RECAPTCHA_PUBLIC_KEY = "6LctfQYAAAAAAH7kNROztNvh1O3DLqBJUFDj9Q-S"
RECAPTCHA_PRIVATE_KEY = "6LctfQYAAAAAACQwyZsp7T0WsvfMwDxdQ2wT4q0v"

YABA_THEME = "default"

###############################################
# end django-yaba specific settings           #
###############################################

DEBUG = True 
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = os.path.join(PROJECT_DIR, 'db/blog-tagging.db')             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = '/home/f4nt/git-repos/personal/django_yaba/media/'
MEDIA_ROOT = os.path.join(PROJECT_DIR, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ROOT_BLOG_URL + "/media/"

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/adminmedia/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'b30u+n8ojd=4a36ivv*2yig#_5vcly#%1j4-v3erg$*8+0u5#9'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'django_yaba.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.comments',
    'tagging',
    'django_yaba.blog'
)

