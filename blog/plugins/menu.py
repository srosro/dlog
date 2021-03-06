"""Menus for plugins"""
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from menus.base import Menu
from menus.base import Modifier
from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu

from blog.models import Entry
from blog.managers import tags_published
from blog.managers import authors_published


class EntryMenu(CMSAttachMenu):
    """Menu for the entries organized by archives dates"""
    name = _('Zinnia Entry Menu')

    def get_nodes(self, request):
        nodes = []
        archives = []
        attributes = {'hidden': True}
        for entry in Entry.published.all():
            year = entry.creation_date.strftime('%Y')
            month = entry.creation_date.strftime('%m')
            month_text = entry.creation_date.strftime('%b')
            day = entry.creation_date.strftime('%d')

            key_archive_year = 'year-%s' % year
            key_archive_month = 'month-%s-%s' % (year, month)
            key_archive_day = 'day-%s-%s-%s' % (year, month, day)

            if not key_archive_year in archives:
                nodes.append(NavigationNode(year, reverse('entry-archive-year', args=[year]),
                                            key_archive_year, attr=attributes))
                archives.append(key_archive_year)

            if not key_archive_month in archives:
                nodes.append(NavigationNode(month_text, reverse('entry-archive-month', args=[year, month]),
                                            key_archive_month, key_archive_year, attr=attributes))
                archives.append(key_archive_month)

            if not key_archive_day in archives:
                nodes.append(NavigationNode(day, reverse('entry-archive-day', args=[year, month, day]),
                                            key_archive_day, key_archive_month, attr=attributes))
                archives.append(key_archive_day)

            nodes.append(NavigationNode(entry.title, entry.get_absolute_url(),
                                        entry.pk, key_archive_day))
        return nodes

class AuthorMenu(CMSAttachMenu):
    """Menu for the authors"""
    name = _('Zinnia Author Menu')

    def get_nodes(self, request):
        nodes = []
        nodes.append(NavigationNode(_('Authors'), reverse('author-list'),
                                    'authors'))
        for author in authors_published():
            nodes.append(NavigationNode(author.username,
                                        reverse('author-detail', args=[author.username]),
                                        author.pk, 'authors'))
        return nodes

class TagMenu(CMSAttachMenu):
    """Menu for the tags"""
    name = _('Zinnia Tag Menu')

    def get_nodes(self, request):
        nodes = []
        nodes.append(NavigationNode(_('Tags'), reverse('tag-list'),
                                    'tags'))
        for tag in tags_published():
            nodes.append(NavigationNode(tag.name,
                                        reverse('tag-detail', args=[tag.name]),
                                        tag.pk, 'tags'))
        return nodes

class EntryModifier(Modifier):
    """Menu Modifier for entries,
    hide the MenuEntry in navigation, not in breadcrumbs"""

    def modify(self, request, nodes, namespace, root_id, post_cut, breadcrumb):
        if breadcrumb:
            return nodes
        for node in nodes:
            if node.attr.get('hidden'):
                nodes.remove(node)
        return nodes


menu_pool.register_menu(EntryMenu)
menu_pool.register_menu(AuthorMenu)
menu_pool.register_menu(TagMenu)
menu_pool.register_modifier(EntryModifier)
