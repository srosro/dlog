"""Urls for the zinnia tags"""
from django.conf.urls.defaults import *

from blog.models import Entry
from blog.managers import tags_published

from django.conf import settings
from settings import PAGINATION


tag_conf = {'queryset': tags_published(),
            'template_name': 'blog/tag_list.html'}

tag_conf_entry = {'queryset_or_model': Entry.published.all(),
                  'paginate_by': PAGINATION,}

t_main = {'queryset_or_model': Entry.published.all(),
                  'paginate_by': PAGINATION,
                  'tag': 'home'}

urlpatterns = patterns('blog.views.tags',
                       url(r'^topics/$', 'tag_list',
                           tag_conf, name='tag-list'),
                       url(r'^$', 'tag_detail',
                           t_main, name='tag-detail'),
                       url(r'^(?P<tag>[-\w]+)/$', 'tag_detail',
                           tag_conf_entry, name='tag-detail'),
                       url(r'^(?P<tag>[-\w]+)/page/(?P<page>\d+)/$',
                           'tag_detail', tag_conf_entry,
                           name='tag-detail-paginated'),
                       )
