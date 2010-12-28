"""Urls for the zinnia feeds"""
from django.conf.urls.defaults import *

from blog.feeds import LatestEntries, CommentEntries, SearchEntries, TagEntries, AuthorEntries

urlpatterns = patterns('',
                       url(r'^latest/$', LatestEntries(),
                           name='zinnia_entry_latest_feed'),
                       url(r'^tags/(?P<slug>[-\w]+)/$', TagEntries(),
                           name='zinnia_tag_feed'),
                       url(r'^authors/(?P<username>[-\w]+)/$', AuthorEntries(),
                           name='zinnia_author_feed'),
                       url(r'^search/(?P<slug>[-\w]+)/$', SearchEntries(),
                           name='zinnia_entry_search_feed'),
                       url(r'^comments/(?P<slug>[-\w]+)/$', CommentEntries(),
                           name='entry_comment_feed'),
                       )

