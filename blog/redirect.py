from django.views.generic.simple import redirect_to
from django.shortcuts import get_object_or_404

from blog.models import Entry

def check(request, url):
    try:
        e = Entry.objects.get(redirect_url=url.rstrip('/'))
        new_url = e.get_absolute_url()
    except Entry.DoesNotExist:
        new_url = '/'
    return redirect_to(request, new_url)