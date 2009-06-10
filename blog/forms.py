from django import forms
from django.db.models import get_model
from django_yaba.blog.widgets import WYMEditor

class ArticleAdminModelForm(forms.ModelForm):
    body = forms.CharField(widget=WYMEditor())

    class Meta:
        model = get_model('django_yaba', 'story')

class GalleryAdminModelForm(forms.ModelForm):
    body = forms.CharField(widget=WYMEditor())

    class Meta:
        model = get_model('django_yaba', 'gallery')
