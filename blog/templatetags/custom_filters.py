from django import template

from utils import convert_to_persian_number


register = template.Library()


@register.filter(name='to_fa_numbers')
def to_fa_numbers(value):
    try:
        return convert_to_persian_number(str(value))
    except:
        return value