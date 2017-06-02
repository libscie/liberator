from django.contrib import admin
from .models import *

class InlinePDFAdmin(admin.StackedInline):
    model = PDF

class InlineIllegalAdmin(admin.StackedInline):
    model = Illegal

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['doi_prefix', 'doi_suffix']
    list_display_links = ['doi_prefix', 'doi_suffix']
    inlines = [InlinePDFAdmin]

