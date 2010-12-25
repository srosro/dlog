from django.conf import settings
from django.contrib.sites.models import Site

def media(request):
    """Adds media-related context variables to the context"""
    return {'MEDIA_URL': settings.MEDIA_URL}

def domain(request):
    """Add domain of project to context"""
    current_site = Site.objects.get_current()
    return {'SITE_DOMAIN': current_site.domain}