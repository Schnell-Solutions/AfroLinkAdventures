from django import template

from destination_cms.css_utils import css_background_image_url

register = template.Library()


@register.filter(name='css_bg_image')
def css_bg_image(url):
    """Safe CSS background-image value for inline styles."""
    return css_background_image_url(url)


@register.simple_tag(takes_context=True)
def localized_text(context, obj, field_base):
    """
    Return obj.<field>_de when language is German and that value is set,
    otherwise obj.<field>_en (with a final fallback to the DE field).
    """
    request = context.get('request')
    language = getattr(request, 'LANGUAGE_CODE', 'en') if request else 'en'
    en_value = getattr(obj, f'{field_base}_en', None) or ''
    de_value = getattr(obj, f'{field_base}_de', None) or ''
    if (language or 'en').startswith('de') and de_value:
        return de_value
    return en_value or de_value
