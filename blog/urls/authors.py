"""URLs for blog authors"""
from django.conf.urls.defaults import *

from blog.managers import authors_published


author_conf = {'queryset': authors_published(),
               'template_name': 'blog/author_list.html',}

urlpatterns = patterns('blog.views.authors',
                       url(r'^$', 'author_list',
                           author_conf, 'author-list'),
                       url(r'^(?P<username>[-\w]+)/$', 'author_detail',
                           name='author-detail'),
                       url(r'^(?P<username>[-\w]+)/page/(?P<page>\d+)/$',
                           'author_detail',
                           name='author-detail-paginated'),
                       )

