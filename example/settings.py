import os
import sys
DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
LIMEHOUSE_PATH = os.path.join(*os.path.split(PROJECT_PATH)[:-1])

sys.path.insert(0, PROJECT_PATH)
sys.path.insert(0, LIMEHOUSE_PATH)

rel = lambda * args: os.path.join(PROJECT_PATH, *args)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'example.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

STATIC_ROOT = rel('static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    rel('site_media'),
)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)
JSTEMPLATES_ROOT = rel('jstemplates')

MIDDLEWARE_CLASSES = ()

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    rel('templates'),
    rel('jstemplates'),
)

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'blog',
    'limehouse',
)
