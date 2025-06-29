from django import template

register = template.Library()

@register.filter
def icon_lookup(icon_map, event_type):
    """Django template filter to look up an icon by event_type, with fallback."""
    return icon_map.get(event_type, '📌')

@register.filter
def dict_lookup(d, key):
    """Django template filter to look up a dictionary value by key."""
    if d and key in d:
        return d[key]
    return ''
