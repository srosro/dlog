"""Settings for testing zinnia"""
from xmlrpc import ZINNIA_XMLRPC_METHODS

SITE_ID = 1

ROOT_URLCONF = 'urls.tests'

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.core.context_processors.request',
    'context_processors.template_settings',
    'context_processors.version',]


DATABASE_ENGINE = 'sqlite3'
INSTALLED_APPS = ['django.contrib.contenttypes',
                  'django.contrib.comments',
                  'django.contrib.sites',
                  'django.contrib.auth',
                  #'south',
                  'django_xmlrpc',
                  'tagging', 'zinnia']

XMLRPC_METHODS = ZINNIA_XMLRPC_METHODS
