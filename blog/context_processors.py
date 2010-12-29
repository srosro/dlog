from django.conf import settings
from django.contrib.sites.models import Site

def template_settings(request):
    """Exposes specific settings to templates"""
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'DISQUS_SHORTNAME': settings.DISQUS_SHORTNAME
    }

def domain(request):
    """Add domain of project to context"""
    current_site = Site.objects.get_current()
    return {'SITE_DOMAIN': current_site.domain}