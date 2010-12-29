"""Models of Zinnia"""
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.defaultfilters import striptags
from django.template.defaultfilters import linebreaks
from django.contrib.comments.moderation import moderator
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField

from moderator import EntryCommentModerator
from blog.managers import entries_published
from blog.managers import EntryPublishedManager
from blog.managers import DRAFT, HIDDEN, PUBLISHED
from blog.misc import get_admin_url
from settings import USE_BITLY, UPLOAD_TO

class Entry(models.Model):
    """Base design for publishing entry"""
    STATUS_CHOICES = ((DRAFT, _('draft')),
                      (HIDDEN, _('hidden')),
                      (PUBLISHED, _('published')))

    title = models.CharField(_('title'), max_length=100)

    image = models.ImageField(_('image'), upload_to=UPLOAD_TO,
                              blank=True, help_text=_('used for illustration'))
    content = models.TextField(_('content'))
    excerpt = models.TextField(_('excerpt'), blank=True,
                                help_text=_('optional element'))

    tags = TagField(_('tags'))
    related = models.ManyToManyField('self', verbose_name=_('related entries'),
                                     blank=True, null=True)

    slug = models.SlugField(help_text=_('used for publication'))
    authors = models.ManyToManyField(User, verbose_name=_('authors'),
                                     blank=True, null=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    comment_enabled = models.BooleanField(_('comment enabled'), default=True)

    creation_date = models.DateTimeField(_('creation date'), default=datetime.now)
    last_update = models.DateTimeField(_('last update'), default=datetime.now)
    start_publication = models.DateTimeField(_('start publication'),
                                             help_text=_('date start publish'),
                                             default=datetime.now)
    end_publication = models.DateTimeField(_('end publication'),
                                           help_text=_('date end publish'),
                                           default=datetime(2042, 3, 15))

    sites = models.ManyToManyField(Site, verbose_name=_('sites publication'))

    objects = models.Manager()
    published = EntryPublishedManager()

    @property
    def html_content(self):
        """Return the content correctly formatted"""
        if not '</p>' in self.content:
            return linebreaks(self.content)
        return self.content

    @property
    def previous_entry(self):
        """Return the previous entry"""
        entries = Entry.published.filter(
            creation_date__lt=self.creation_date)
        if entries:
            return entries[0]

    @property
    def next_entry(self):
        """Return the next entry"""
        entries = Entry.published.filter(
            creation_date__gt=self.creation_date).order_by('creation_date')
        if entries:
            return entries[0]

    @property
    def word_count(self):
        """Count the words of an entry"""
        return len(striptags(self.html_content).split())

    @property
    def is_actual(self):
        """Check if an entry is within publication period"""
        now = datetime.now()
        return now >= self.start_publication and now < self.end_publication

    @property
    def is_visible(self):
        """Check if an entry is visible on site"""
        return self.is_actual and self.status == PUBLISHED

    @property
    def related_published_set(self):
        """Return only related entries published"""
        return entries_published(self.related)

    @property
    def comments(self):
        """Return published comments"""
        from django.contrib.comments.models import Comment
        return Comment.objects.for_model(self).filter(is_public=True)

    def __unicode__(self):
        return '%s: %s' % (self.title, self.get_status_display())

    @models.permalink
    def get_absolute_url(self):
        return ('zinnia_entry_detail', (), {
            'year': self.creation_date.strftime('%Y'),
            'month': self.creation_date.strftime('%m'),
            'day': self.creation_date.strftime('%d'),
            'slug': self.slug})

    def get_admin_url(self):
        import pdb; pdb.set_trace()
        return get_admin_url(self)
        
    class Meta:
        ordering = ['-creation_date']
        verbose_name = _('entry')
        verbose_name_plural = _('entries')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )

moderator.register(Entry, EntryCommentModerator)
