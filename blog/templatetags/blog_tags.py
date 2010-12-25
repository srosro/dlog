"""Template tags for Zinnia"""
try:
    from hashlib import md5
except ImportError:
    from md5 import new as md5

from random import sample
from urllib import urlencode
from datetime import datetime

from django.template import Library

from blog.models import Entry
from blog.comparison import VectorBuilder
from blog.comparison import pearson_score

register = Library()

vectors = VectorBuilder({'queryset': Entry.published.all(),
                        'fields': ['title', 'excerpt', 'content']})
cache_entries_related = {}

@register.inclusion_tag('blog/tags/recent_entries.html')
def get_recent_entries(number=5):
    """Return the most recent entries"""
    return {'entries': Entry.published.all()[:number]}

@register.inclusion_tag('blog/tags/random_entries.html')
def get_random_entries(number=5):
    """Return random entries"""
    entries = Entry.published.all()
    if number > len(entries):
        number = len(entries)
    return {'entries': sample(entries, number)}

@register.inclusion_tag('blog/tags/popular_entries.html')
def get_popular_entries(number=5):
    """Return popular  entries"""
    entries_comment = [(e, e.comments.count()) for e in Entry.published.all()]
    entries_comment = sorted(entries_comment, key=lambda x: (x[1], x[0]),
                             reverse=True)[:number]
    entries = [entry for entry, n_comments in entries_comment]
    return {'entries': entries}

@register.inclusion_tag('blog/tags/similar_entries.html', takes_context=True)
def get_similar_entries(context, number=5):
    """Return similar entries"""
    global vectors
    global cache_entries_related

    def compute_related(object_id, dataset):
        object_vector = None
        for entry, e_vector in dataset.items():
            if entry.pk == object_id:
                object_vector = e_vector

        if not object_vector:
            return []

        entry_related = {}
        for entry, e_vector in dataset.items():
            if entry.pk != object_id:
                score = pearson_score(object_vector, e_vector)
                if score:
                    entry_related[entry] = score

        related = sorted(entry_related.items(), key=lambda(k,v):(v,k))
        return [i for i, s in related]

    object_id = context['object'].pk
    columns, dataset = vectors()
    key = '%s-%s' % (object_id, vectors.key)
    if not key in cache_entries_related.keys():
        cache_entries_related[key] = compute_related(object_id, dataset)

    entries = cache_entries_related[key][:number]
    return {'entries': entries}


@register.inclusion_tag('blog/tags/dummy.html')
def get_archives_entries(template='blog/tags/archives_entries.html'):
    """Return archives entries"""
    return {'template': template,
            'archives': Entry.published.dates('creation_date', 'month',
                                              order='DESC'),}

@register.inclusion_tag('blog/tags/breadcrumbs.html', takes_context=True)
def zinnia_breadcrumbs(context, separator='/', root_name='Blog'):                       
    """Return a breadcrumb for the application"""
    from blog.templatetags.zbreadcrumbs import retrieve_breadcrumbs

    path = context['request'].path
    page_object = context.get('object') or \
                  context.get('tag') or \
                  context.get('author')
    breadcrumbs = retrieve_breadcrumbs(path, page_object, root_name)

    return {'separator': separator,
            'breadcrumbs': breadcrumbs}

@register.simple_tag
def get_gravatar(email, size, rating, default=None):
    """Return url for a Gravatar"""
    url = 'http://www.gravatar.com/avatar/%s.jpg' % md5(email).hexdigest()
    options = {'s': size, 'r': rating}
    if default:
        options['d'] = default

    url = '%s?%s' % (url, urlencode(options))
    return url.replace('&', '&amp;')

