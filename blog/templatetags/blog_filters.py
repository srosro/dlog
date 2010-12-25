from django import template
from django.utils.text import truncate_html_words
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter(name='truncate_entry')
def truncate_entry(entry, words=100):
    end_text = '... <a href="%s">more</a>' % entry.get_absolute_url()
    content = entry.html_content
    try:
        return truncate_html_words(content, int(words), end_text=end_text)
    except ValueError: # invalid literal for int()
        return value # Fail silently.
truncate_entry.is_safe = True
