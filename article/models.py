# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import mptt
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from embed_video.fields import EmbedVideoField
from mptt.models import MPTTModel, TreeForeignKey


class Keywords(models.Model):
    class Meta():
        db_table = "keywords"
    name = models.CharField(max_length=50, blank=True, unique=True, verbose_name="Tags")

    def __unicode__(self):
        return self.name


class Category(MPTTModel):
    class Meta():
        db_table = "category"
        verbose_name_plural = "Categories"
        verbose_name = "Category"
        ordering = ('tree_id', 'level',)
    name = models.CharField(max_length=150, verbose_name="Category", unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="Parent's class")

    def __unicode__(self):
        return self.name

    class MPTTMeta:
        level_atrr = 'mptt-level'
        order_insertion_by = ['name']


mptt.register(Category, order_insertion_by=['name'])


class Article(models.Model):
    class Meta():
        db_table = "article"

    article_title = models.CharField(max_length=200)
    article_text = RichTextField()
    article_date = models.DateTimeField()
    article_likes = models.IntegerField(default=0)
    article_image = models.ImageField(null=True, blank=True, upload_to="images/", verbose_name="Image")
    video = EmbedVideoField(null=True, blank=True, verbose_name="Video")
    category = TreeForeignKey(Category, null=True, blank=False, related_name='cat')
    keywords = models.ManyToManyField(Keywords, related_name="keywords", related_query_name="keywords", blank=True, verbose_name="Keywords")


    def __unicode__(self):
        return self.article_title

    def bit(self):
        if self.article_image:
            return u'<img src="{0}" width="100"/>'.format(self.article_image.url)
        else:
            return u'(none)'
        bit.short_description = "Image"
        bit.allow_tags = True


class Comments(models.Model):
    class Meta():
        db_table = "comments"

    comments_text = RichTextField(verbose_name="Comment's text")
    comments_article = models.ForeignKey(Article)
    comments_date = models.DateTimeField(u'date', auto_now_add=True)
    comments_author = models.ForeignKey(User)
