"""Urls for the zinnia search"""
from django.conf.urls.defaults import *

urlpatterns = patterns('blog.views.search',
                       url(r'^$', 'entry_search', name='zinnia_entry_search'),
                       )
