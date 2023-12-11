from django import template

register = template.Library()


@register.inclusion_tag('labapp/apply_table.html')
def apply_table(applies):
    return {'applies': applies}
