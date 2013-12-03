from django import template
from django.template.loader import add_to_builtins


register = template.Library()

@register.filter(name='classname')
def classname(obj):
	classname = obj.__class__.__name__
	return classname

add_to_builtins('website.templatetags.extra_tags')