from django import template
from django.conf import settings

register = template.Library()

class SettingObjectNode(template.Node):
    """
    TODO: Documentation
    """
    def __init__(self, setting_name, var_name):
        self.setting_name = setting_name
        self.var_name = var_name

    def render(self, context):
        try:
            setting = getattr(settings, self.setting_name)
        except:
            raise TemplateSyntaxError, "Setting doesn't exist"

        if self.var_name is None:
            self.var_name = setting_name
        context.update({self.var_name: setting})
        return ''

@register.tag
def get_setting(parser, token):
    """
    USAGE:
    "variable name" is optional
    {% load get_setting %}
      {% get_setting "SETTING_NAME" "variable_name" %}

    EXAMPLE:
    {% load get_setting %}
      {% get_setting "LOGIN_URL" "login_path" %}
        {{ login_path }}
    """
    try:
        tag_name, setting_name, var_name = token.split_contents()
    except ValueError:
        if var_name is None and setting_name is not None:
            var_name = setting_name
        else:
            raise template.TemplateSyntaxError("Setting Tag requires 1 variables")

    return SettingObjectNode(setting_name[1:-1], var_name[1:-1])
