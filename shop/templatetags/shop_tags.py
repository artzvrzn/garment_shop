from django import template
from django.db.models import *
from shop.models import *

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()

