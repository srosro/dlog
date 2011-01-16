from django.db.models import permalink
from django.contrib.contenttypes.models import ContentType

@permalink
def get_admin_url(obj):
    "Returns the URL to the object in the Django admin site."
    content_type = ContentType.objects.get_for_model(obj)
    return ('django.contrib.admin.views.main.change_stage', 
            [content_type.app_label, content_type.model, str(obj.pk)])
