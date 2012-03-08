# Create your views here.
from django.contrib.auth import logout, login, authenticate
from django.http import  HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.views.generic.simple import direct_to_template
from Allthink.forms import *
from Allthink.models import *


def user_page(request, username):
    user = get_object_or_404(User, username=username)
    variables = RequestContext(request, {
        'username': username,
    })
    return  render_to_response('user_page.html', variables)

def main_page(request):
    return render_to_response(
        'main_page.html', RequestContext(request)
    )

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def register_page(request):
    return render_to_response('registration/signup.html', RequestContext(request))

def teacher_register_page(request) :
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                fullname=form.cleaned_data['fullname'],
                typeUser='teacher',
            )
            return render_to_response('registration/teacher_signup_success.html', RequestContext(request))
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/teacher_signup.html',variables)

def student_register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                fullname=form.cleaned_data['fullname'],
                typeUser='teacher',
            )
            return render_to_response('registration/teacher_signup_success.html', RequestContext(request))
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/student_signup.html',variables)