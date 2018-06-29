from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from article import views as article_views

urlpatterns = [
    url(r'^1/', article_views.basic_one, name='basic_one'),
    url(r'^2/', article_views.template_two, name='template_two'),
    url(r'^3/', article_views.template_three_simple, name='template_three'),
    url(r'^articles/all/$', article_views.articles, name='articles'),
    url(r'^articles/get/(?P<article_id>\d+)/$', article_views.article, name='article'),
    url(r'^articles/addlike/(?P<article_id>\d+)/$', article_views.addlike, name='addlike'),
    url(r'^articles/addcomment/(?P<article_id>\d+)/$', article_views.addcomment, name='addcomment'),
    url(r'^page/(\d+)/$', article_views.articles, name='articles'),
    url(r'^category/get/(?P<category_id>\d+)/$', article_views.article_cat, name='article_cat'),
    url(r'^keyword/(?P<id>\d+)/$', article_views.keywords, name='keywords'),
    url(r'^$', article_views.articles, name='articles'),

]

if settings.DEBUG:
    if settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += staticfiles_urlpatterns()