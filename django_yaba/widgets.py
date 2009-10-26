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
            '''
            tinyMCE.init({
                mode : "textareas",
                theme : "advanced",
                editor_selector : "tinymce",
                theme_advanced_buttons1 : "formatselect, bold, italic, strikethrough, sub, sup, charmap, bullist, numlist,
                    indent, outdent, link, unlink, undo, redo, code",
                theme_advanced_buttons2 : "",
                theme_advanced_blockformats : "p, h2, h3, h4, h5, h6, blockquote",
                theme_advanced_toolbar_location : "top"
            });
            ''',
        )

class SmallTextField(forms.Textarea):
    def render(self, name, value, attrs=None):
        self.attrs = {'rows': '3','cols': '50'}
        output = [super(SmallTextField, self).render(name, value, attrs)]
        return mark_safe(u''.join(output))
