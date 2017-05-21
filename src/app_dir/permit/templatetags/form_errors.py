from django import template

register = template.Library()


@register.inclusion_tag('template_tags/form_errors.html')
def form_errors(form):
    return {'form': form}
