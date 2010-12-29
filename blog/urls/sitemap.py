"""Urls for the zinnia sitemap"""
from django.conf.urls.defaults import *

urlpatterns = patterns('blog.views.sitemap',
                       url(r'^$', 'sitemap',
                           {'template': 'blog/sitemap.html'},
                           name='zinnia-sitemap'),
                       )


