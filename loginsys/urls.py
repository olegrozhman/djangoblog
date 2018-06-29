from django.conf.urls import include, url
from loginsys import views as loginsys_views

urlpatterns = [
    url(r'^login/', loginsys_views.login, name='login'),
    url(r'^logout/', loginsys_views.logout, name='logout'),
    url(r'^register/', loginsys_views.register, name='register'),
]