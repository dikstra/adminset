#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from accounts.forms import LoginUserForm, ChangePasswordForm
from django.urls import reverse


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'GET' and request.GET['next']:
        next_page = request.GET['next']
    else:
        next_page = '/'
    if next_page == "/accounts/logout/":
        next_page = '/'
    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect(request.POST['next'])
    else:
        form = LoginUserForm(request)
    kwargs = {
        'request': request,
        'form':  form,
        'next': next_page,
    }
    return render(request, 'accounts/login.html', kwargs)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def change_password(request):
    temp_name = "accounts/accounts-header.html"
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'accounts/password_confirm.html', locals())
    else:
        form = ChangePasswordForm(user=request.user)
    kwargs = {
        'form': form,
        'request': request,
        'temp_name': temp_name,
    }
    return render(request, 'accounts/change_password.html', kwargs)

