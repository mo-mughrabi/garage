from django import template
import logging
from django.conf import settings

register = template.Library()
logging.getLogger(__name__)


@register.filter
def i18n(obj, language):
    return obj.i18n(language)

@register.filter
def is_model_i18n_healthy(queryset):
    try:
        languages=getattr(settings, 'LANGUAGES')
        if queryset.count() != len(languages):
            return False
        else:
            return True
    except Exception as e:
        logging.error(str(e))