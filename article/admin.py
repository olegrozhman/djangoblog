# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import mptt
from django.contrib import admin

from article.models import Article, Comments, Keywords
from .models import Category


class ArticleInline(admin.StackedInline):
    model = Comments
    extra = 2


class ArticleAdmin(admin.ModelAdmin):
    fields = ['article_title', 'article_text', 'article_date', 'article_image', 'video', 'category', 'keywords']
    list_display = ['article_title', 'article_date', 'article_image', 'bit', 'category']
    readonly_fields = ['bit']
    inlines = [ArticleInline]
    list_filter = ['category']
    search_fields = ['article_title']


class CategoryAdmin(admin.ModelAdmin):
    fields = ['parent', 'name']


class KeywordsAdmin(admin.ModelAdmin):
    fields = ['name']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Keywords, KeywordsAdmin)
