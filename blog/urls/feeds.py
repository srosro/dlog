"""Urls for the zinnia feeds"""
from django.conf.urls.defaults import *

from blog.feeds import LatestEntries, CommentEntries, SearchEntries, TagEntries, AuthorEntries

urlpatterns = patterns('',
                       url(r'^latest/$', LatestEntries(),
                           name='entry-latest-feed'),
                       url(r'^tags/(?P<slug>[-\w]+)/$', TagEntries(),
                           name='tag-feed'),
                       url(r'^authors/(?P<username>[-\w]+)/$', AuthorEntries(),
                           name='author-feed'),
                       url(r'^search/(?P<slug>[-\w]+)/$', SearchEntries(),
                           name='entry-search-feed'),
                       url(r'^comments/(?P<slug>[-\w]+)/$', CommentEntries(),
                           name='entry-comment-feed'),
                       )

