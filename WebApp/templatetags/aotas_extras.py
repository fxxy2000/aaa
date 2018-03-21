from django import template
from DataModel.AppInfo import AppInfo

register = template.Library()

@register.filter(name='localize_category')
def localize_category(app_info, risk_category):
    return app_info.get_localized_category(risk_category)

@register.filter
def replace_dot(value, replacement):
    return value.replace(".",replacement)