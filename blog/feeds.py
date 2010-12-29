"""Feeds for Zinnia"""
from datetime import datetime
from sgmllib import SGMLParser

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.comments.models import Comment
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404

from tagging.models import Tag
from tagging.models import TaggedItem

from blog.models import Entry
from blog.managers import entries_published
from settings import COPYRIGHT


current_site = Site.objects.get_current()

class ImgParser(SGMLParser):
    """Parser for getting img markups"""

    def __init__(self):
        SGMLParser.__init__(self)
        self.img_locations = []

    def start_img(self, attr):
        attr = dict(attr)
        if attr.get('src', ''):
            self.img_locations.append(attr['src'])


class EntryFeed(Feed):
    """Base Entry Feed"""
    title_template = 'feeds/entry_title.html'
    description_template= 'feeds/entry_description.html'
    feed_copyright = COPYRIGHT

    def item_pubdate(self, item):
        return item.creation_date

    def item_author_name(self, item):
        return item.authors.all()[0].get_full_name()

    def item_author_email(self, item):
        return item.authors.all()[0].email

    def item_author_link(self, item):
        return current_site.domain

    def item_enclosure_url(self, item):
        if item.image:
            return item.image.url
        parser = ImgParser()
        try:
            parser.feed(item.content)
        except UnicodeEncodeError:
            return
        if len(parser.img_locations):
            if current_site.domain in parser.img_locations[0]:
                return parser.img_locations[0]
            else:
                return 'http://%s%s' % (
                    current_site.domain, parser.img_locations[0])
        return None

    def item_enclosure_length(self, item):
        return '100000'

    def item_enclosure_mime_type(self, item):
        return 'image/jpeg'


class LatestEntries(EntryFeed):
    """Feed for the latest entries"""
    title = _('Latest entries')
    description = _('The latest entries for the site %s') % current_site.domain

    def link(self):
        return reverse('entry-archive-index')

    def items(self):
        return Entry.published.all()

class AuthorEntries(EntryFeed):
    """Feed filtered by an author"""

    def get_object(self, request, username):
        return get_object_or_404(User, username=username)

    def items(self, obj):
        return entries_published(obj.entry_set)

    def link(self, obj):
        return reverse('author-detail', args=[obj.username])

    def title(self, obj):
        return _('Entries for author %s') % obj.username

    def description(self, obj):
        return _('The latest entries by %s') % obj.username


class TagEntries(EntryFeed):
    """Feed filtered by a tag"""

    def get_object(self, request, slug):
        return get_object_or_404(Tag, name=slug)

    def items(self, obj):
        return TaggedItem.objects.get_by_model(Entry.published.all(), obj)

    def link(self, obj):
        return reverse('tag-detail', args=[obj.name])

    def title(self, obj):
        return _('Entries for the tag %s') % obj.name

    def description(self, obj):
        return _('The latest entries for the tag %s') % obj.name


class SearchEntries(EntryFeed):
    """Feed filtered by search pattern"""

    def get_object(self, request, slug):
        return slug

    def items(self, obj):
        return Entry.published.search(obj)

    def link(self, obj):
        return '%s?pattern=%s' % (reverse('entry-search'), obj)

    def title(self, obj):
        return _("Results of the search for %s") % obj

    def description(self, obj):
        return _("The entries containing the pattern %s") % obj


class CommentEntries(Feed):
    """Feed for comments in an entry"""
    title_template = 'feeds/comment_title.html'
    description_template= 'feeds/comment_description.html'
    feed_copyright = COPYRIGHT

    def get_object(self, request, slug):
        return get_object_or_404(Entry, slug=slug)

    def items(self, obj):
        return Comment.objects.for_model(obj).order_by('-submit_date')[:10]

    def item_pubdate(self, item):
        return item.submit_date

    def item_link(self, item):
        return item.get_absolute_url('#comment_%(id)s')

    def link(self, obj):
        return obj.get_absolute_url()

    def item_author_name(self, item):
        return item.userinfo['name']

    def item_author_email(self, item):
        return item.userinfo['email']

    def item_author_link(self, item):
        return item.userinfo['url']

    def title(self, obj):
        return _('Comments on %s') % obj.title

    def description(self, obj):
        return _('The latest comments for the entry %s') % obj.title