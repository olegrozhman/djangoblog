# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response, redirect, render

from django.http.response import HttpResponse, Http404
from django.template.loader import get_template
from article.models import Article, Comments, Category, Keywords
from django.core.exceptions import ObjectDoesNotExist
from django.template.context_processors import csrf
from .forms import CommentForm
from django.core.paginator import Paginator
from django.contrib import auth


def basic_one(request):
    view = "basic_one"
    html = "<html><body>This is %s view</html></body>" % view
    return HttpResponse(html)


def template_two(request):
    view = "template_two"
    t = get_template('myview.html')
    html = t.render({'name': view})
    return HttpResponse(html)


def template_three_simple(request):
    view = "template_three"
    return render_to_response('myview.html', {'name': view})


def articles(request, page_number=1):
    all_articles = Article.objects.all().order_by('-id')
    current_page = Paginator(all_articles, 3)
    return render_to_response('articles.html',
                              {'articles': current_page.page(page_number), 'projects': Category.objects.all(),
                               'keywords': Keywords.objects.all(), 'username': auth.get_user(request).username})


def article(request, article_id=1):
    comment_form = CommentForm
    args = {}
    args.update(csrf(request))
    args['projects'] = Category.objects.all()
    args['article'] = Article.objects.get(id=article_id)
    args['category'] = Category.objects.filter(id=article_id)
    args['comments'] = Comments.objects.filter(comments_article_id=article_id).order_by('-id')
    args['form'] = comment_form
    args['keywords'] = Keywords.objects.all()
    args['username'] = auth.get_user(request).username
    return render_to_response('article.html', args)


def addlike(request, article_id):
    try:
        if article_id in request.COOKIES:
            return_path = request.META.get(
                'HTTP_REFERER', '/')
            return redirect(return_path)
        else:
            article = Article.objects.get(id=article_id)
            article.article_likes += 1
            article.save()
            return_path = request.META.get(
                'HTTP_REFERER', '/')
            response = redirect(return_path)
            response.set_cookie(article_id, "test")
            return response
    except ObjectDoesNotExist:
        raise Http404
    return redirect('/')


def addcomment(request, article_id):
    if request.POST and ("pause" not in request.session):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comments_author = request.user
            comment.comments_article = Article.objects.get(id=article_id)
            form.save()
            request.session.set_expiry(60)
            request.session['pause'] = True
    return redirect('/articles/get/%s/' % article_id)


def article_cat(request, category_id=1):
    args = {}
    args['projects'] = Category.objects.all()
    args['category'] = Category.objects.get(id=category_id)
    branch_categories = args['category'].get_descendants(include_self=True)
    args['articles'] = Article.objects.filter(category_id=category_id)
    args['username'] = auth.get_user(request).username
    args['keywords'] = Keywords.objects.all()
    args['category_articles'] = Article.objects.filter(category__in=branch_categories).distinct()
    return render_to_response('article_cat.html', args)


def keywords(request, id):
    args = {}
    args['keywords'] = Keywords.objects.all()
    args['keyw_s'] = Keywords.objects.get(id=id)
    args['articles'] = Article.objects.filter(keywords__name__exact=args['keyw_s'])
    args['projects'] = Category.objects.all()
    args['username'] = auth.get_user(request).username
    return render(request, 'keywpage.html', args)
