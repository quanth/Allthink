# Create your views here.
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import  HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from Allthink.forms import *
from Allthink.models import *

@login_required
def user_page(request, username):
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'teacher' :
        lessions = user_profile.lesson_set.all()
        variables = RequestContext(request, {
            'username': username,
                'lessions': lessions,
        })
        return  render_to_response('teacher_page.html', variables)
    else :
        # hien tai chua co student user
        return render_to_response('teacher_page.html')


def main_page(request):
    return render_to_response(
        'main_page.html', RequestContext(request)
    )

def login(request):
    status='Wellcome !'
    if request.method== "POST":
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            login_username=login_form.cleaned_data['username']
            login_password=login_form.cleaned_data['password']
            user = auth.authenticate(username=login_username, password=login_password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/user/'+login_username+'/')
            else:
                status="This user is not exits !"
            variables=RequestContext(request,{
                'form': login_form,
                'status':status,
            })
            return render_to_response('registration/login.html',variables)
    else :
        login_form=LoginForm()
    variables= RequestContext(request,{
        'form':login_form,
        'status':status
    })
    return render_to_response('registration/login.html',variables)

def logout_page(request):
    logout(request)
    return render_to_response('registration/logout.html')

def register_page(request):
    return render_to_response('registration/signup.html', RequestContext(request))

def teacher_register_page(request) :
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
            )
            user_profile = UserProfile.objects.create(
                user = user,
                fullname=form.cleaned_data['fullname'],
                typeUser='teacher',
            )
            return render_to_response('registration/teacher_signup_success.html', RequestContext(request))
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/teacher_signup.html',variables)

def create_lesson(request, username) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if request.method == 'POST' :
        form = CreateLesson(request.POST)
        if form.is_valid() :
            lesson = Lesson.objects.create(
                lessonTitle = form.cleaned_data['lessonTitle'],
                gradeLevel = form.cleaned_data['gradeLevel'],
                subject = form.cleaned_data['subject'],
            )
            return render_to_response('lesson/create_lesson.html', RequestContext(request))
    else :
        form = CreateLesson()
    variables = RequestContext(request, {'form' : form})
    return render_to_response('lesson/create_lesson.html',variables)