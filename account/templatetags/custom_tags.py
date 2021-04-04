from django import template

register = template.Library()


@register.inclusion_tag('account/partials/link.html')
def link(request, link_url, content, font_icon):
    return {
        'request': request,
        'link_url': link_url,
        'content': content,
        'font_icon': font_icon,
    }
