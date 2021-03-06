"""Defaults urls for the zinnia project"""
from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       url(r'^feeds/', include('blog.urls.feeds')),
                       url(r'^authors/', include('blog.urls.authors')),
                       url(r'^search/', include('blog.urls.search')),
                       url(r'^sitemap/', include('blog.urls.sitemap')),
                       url(r'^comments/', include('django.contrib.comments.urls')),
                       url(r'^', include('blog.urls.entries')),

                       #Make tags top-level.  NOTE: this means they might conflict with
                       #blog articles, which are in the same namespace.
                       url(r'^', include('blog.urls.tags',)),
                       )

