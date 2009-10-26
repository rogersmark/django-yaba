from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

class TinyMCEWidget(forms.Textarea):
    def render(self, name, value, attrs=None):
        self.attrs = {'class': 'tinymce vLargeTextField', 'rows': '16','cols': '40'}
        output = [super(TinyMCEWidget, self).render(name, value, attrs)]
        return mark_safe(u''.join(output))

    class Media:
        js = (
            settings.MEDIA_URL + 'js/tiny_mce/tiny_mce.js',
            settings.MEDIA_URL + 'js/textareas.js',
        )

class SmallTextField(forms.Textarea):
    def render(self, name, value, attrs=None):
        self.attrs = {'rows': '3','cols': '50'}
        output = [super(SmallTextField, self).render(name, value, attrs)]
        return mark_safe(u''.join(output))
