from django.contrib import admin
from .models import *

class InlinePDFAdmin(admin.StackedInline):
	model = PDF

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	inlines = [InlinePDFAdmin]