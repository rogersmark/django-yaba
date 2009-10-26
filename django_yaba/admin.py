from django.contrib import admin
from django_yaba import forms
from django_yaba.models import *

class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 10

class ItemAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]

class ThemeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class ConfigurationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class GalleryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PhotoInline]
    form = forms.GalleryAdminForm

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('label',)}

class LinksAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('label',)}
    list_filter = ('label', 'site_link')
    search_fields = ('label', 'site_link')

class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'created', 'modified')
    search_fields = ('title', 'content')
    list_filter = ('status', 'owner', 'created', 'modified')
    prepopulated_fields = {'slug': ('title',)}
    form = forms.StoryAdminForm

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'created', 'modified')
    search_fields = ('title', 'content')
    list_filter = ('status', 'owner', 'created', 'modified')
    prepopulated_fields = {'slug': ('title',)}
    form = forms.ArticleAdminForm

admin.site.register(Story, StoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Links, LinksAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Configuration, ConfigurationAdmin)
