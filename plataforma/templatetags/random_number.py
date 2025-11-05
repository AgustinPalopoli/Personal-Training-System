import random
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def random_int(a, b=None):
    if b is None:
        a, b = 0, a
    direccion = "static/plataforma/imageDesign/" + str(random.randint(a, b)) + ".jpg"
    return direccion

@register.filter
def tiempo_str(hora):
    if str(hora) != "0:00:00":
        return True