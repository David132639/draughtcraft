from django import template
from django.template.defaultfilters import stringfilter
import re
register = template.Library()


def getSplit(arg):
	matches = [match.start(0) for match in re.finditer(" ",arg)]
	matches.sort(key=lambda x: abs(x-250))
	print(matches[0])
	return matches[0]


@register.filter
@stringfilter
def getShort(arg):
	return arg[:getSplit(arg)]

@register.filter
@stringfilter
def getLong(arg):
	return arg[getSplit(arg):]


