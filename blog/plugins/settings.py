"""Settings of Zinnia.plugins"""
from django.conf import settings

PLUGINS_TEMPLATES = getattr(settings, 'ZINNIA_PLUGINS_TEMPLATES', [])
try:
    from plugins.menu import EntryMenu
    from plugins.menu import TagMenu
    from plugins.menu import AuthorMenu

    APP_MENUS = getattr(settings, 'ZINNIA_APP_MENUS', [EntryMenu,
                                                       TagMenu,
                                                       AuthorMenu])
except ImportError:
    APP_MENUS = []



