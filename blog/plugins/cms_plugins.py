"""Plugins for CMS"""
from django.utils.translation import ugettext as _

from tagging.models import TaggedItem
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from blog.models import Entry
from blog.managers import tags_published
from blog.managers import authors_published
from plugins.models import LatestEntriesPlugin
from plugins.models import SelectedEntriesPlugin
from settings import MEDIA_URL

class CMSLatestEntriesPlugin(CMSPluginBase):
    module = _('entries')
    model = LatestEntriesPlugin
    name = _('Latest entries')
    render_template = 'blog/cms/entry_list.html'
    filter_horizontal = ['authors', 'tags']
    fieldsets = ((None, {'fields': ('number_of_entries', 'template_to_render')}),
                 (_('Sorting'), {'fields': ('authors', 'tags'),
                                 'classes': ('collapse',)}),)
    text_enabled = True

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'authors':
            kwargs['queryset'] = authors_published()
        if db_field.name == 'tags':
            kwargs['queryset'] = tags_published()
        return super(CMSLatestEntriesPlugin, self).formfield_for_manytomany(
            db_field, request, **kwargs)

    def render(self, context, instance, placeholder):
        entries = Entry.published.all()

        if instance.authors.count():
            entries = entries.filter(authors__in=instance.authors.all())
        if instance.tags.count():
            entries = TaggedItem.objects.get_union_by_model(
                entries, instance.tags.all())

        entries = entries[:instance.number_of_entries]
        context.update({'entries': entries,
                        'object': instance,
                        'placeholder': placeholder})
        return context

    def icon_src(self, instance):
        return MEDIA_URL + u'img/plugin.png'

class CMSSelectedEntriesPlugin(CMSPluginBase):
    module = _('entries')
    model = SelectedEntriesPlugin
    name = _('Selected entries')
    render_template = 'blog/cms/entry_list.html'
    fields = ('entries', 'template_to_render')
    filter_horizontal = ['entries']
    text_enabled = True

    def render(self, context, instance, placeholder):
        context.update({'entries': instance.entries.all(),
                        'object': instance,
                        'placeholder': placeholder})
        return context

    def icon_src(self, instance):
        return MEDIA_URL + u'img/plugin.png'

plugin_pool.register_plugin(CMSLatestEntriesPlugin)
plugin_pool.register_plugin(CMSSelectedEntriesPlugin)
