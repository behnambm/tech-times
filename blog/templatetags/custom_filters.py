from django import template

from utils import convert_to_persian_number, convert_to_jalali


register = template.Library()


@register.filter(name='to_fa_numbers')
def to_fa_numbers(value):
    try:
        return convert_to_persian_number(str(value))
    except:
        return value


@register.filter(name='none_to')
def none_to(value, to):
    if not value:
        return to
    return value


@register.filter(name='to_jalali_datetime')
def to_jalali_datetime(value):
    try:
        return convert_to_jalali(value)
    except:
        return value
