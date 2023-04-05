from django import template
from django.utils.text import slugify
from unidecode import unidecode

register = template.Library()


@register.filter(name='slugify_unicode')
def slugify_unicode(value):
    value = unidecode(value)
    return slugify(value, True)
