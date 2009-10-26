from django import forms
from django.db.models import get_model
from django_yaba import widgets

class StoryAdminForm(forms.ModelForm):
    body=forms.CharField(widget=widgets.TinyMCEWidget())

    class Meta:
        model = get_model('django_yaba', 'story')

class ArticleAdminForm(forms.ModelForm):
    body=forms.CharField(widget=widgets.TinyMCEWidget())

    class Meta:
        model = get_model('django_yaba', 'article')

class GalleryAdminForm(forms.ModelForm):
    body=forms.CharField(widget=widgets.TinyMCEWidget())

    class Meta:
        model = get_model('django_yaba', 'gallery')

