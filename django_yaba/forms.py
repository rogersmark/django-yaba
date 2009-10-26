from django import forms
from django.db.models import get_model
from django_yaba import widgets

class StoryAdminForm(models.ModelForm):
    body=forms.CharField(widget=widgets.TinyMCEWidget())

    class Meta:
        model = get_model('django_yaba', 'story')

class ArticleAdminForm(models.ModelForm):
    body=forms.CharField(widget=widgets.TinyMCEWidget())

    class Meta:
        model = get_model('django_yaba', 'article')

class GalleryAdminForm(models.ModelForm):
    body=forms.CharField(widget=widgets.TinyMCEWidget())

    class Meta:
        model = get_model('django_yaba', 'gallery')

