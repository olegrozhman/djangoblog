# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from article.models import Category, Keywords


def login(request):
    args = {}
    args['projects'] = Category.objects.all()
    args['keywords'] = Keywords.objects.all()
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "No such user"
            return render_to_response('login.html', args)
    else:
        return render_to_response('login.html', args)


def logout(request):
    return_path = request.META.get(
        'HTTP_REFERER', '/')
    auth.logout(request)
    return redirect(return_path)


def register(request):
    args = {}
    args['projects'] = Category.objects.all()
    args['keywords'] = Keywords.objects.all()
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                        password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render_to_response('register.html', args)
