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
        lessons = user_profile.lesson_set.all()
        variables = RequestContext(request, {
            'username': username,
            'fullname' : user_profile.fullname,
            'lessons': lessons,
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
                typeUser="teacher",
            )
            return render_to_response('registration/teacher_signup_success.html', RequestContext(request))
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/teacher_signup.html',variables)

@login_required
def create_lesson(request, username) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if request.method == 'POST' :
        form = CreateLesson(request.POST)
        if form.is_valid() :
            lesson = Lesson.objects.create(
                user = user_profile,
                lessonTitle = form.cleaned_data['lessonTitle'],
                gradeLevel = form.cleaned_data['gradeLevel'],
                subject = form.cleaned_data['subject'],
                description = form.cleaned_data['description'],
            )
            variables = RequestContext ( request,{
                'username' : username,
                'fullname' : user_profile.fullname,
                'lesson'   : lesson
            })
            return render_to_response('lesson/lesson_edit.html', variables)
    else :
        form = CreateLesson()
    variables = RequestContext(request,{
        'form' : form,
        'fullname' : user_profile.fullname,
        'username' : username,
    })
    return render_to_response('lesson/create_lesson.html',variables)

@login_required
def edit_lesson(request, username, id) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    lesson = get_object_or_404(Lesson, id = id)
    videos = lesson.video_set.all()
    docs = lesson.document_set.all()
    images = lesson.image_set.all()
    steps = lesson.stepbystep_set.all()
    texts = lesson.text_set.all()
    variables = RequestContext ( request,{
        'username' : username,
        'fullname' : user_profile.fullname,
        'lesson'   : lesson,
        'videos' : videos,
        'docs' : docs,
        'images' : images,
        'steps' : steps,
        'texts' : texts,
    })
    return render_to_response('lesson/lesson_edit.html',variables)

@login_required
def view_lesson(request, username, id, page) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    lesson = get_object_or_404(Lesson, id = id)
    videos = lesson.video_set.all()
    docs = lesson.document_set.all()
    images = lesson.image_set.all()
    steps = lesson.stepbystep_set.all()
    texts = lesson.text_set.all()
    variables = RequestContext ( request,{
        'username' : username,
        'page' : page,
        'fullname' : user_profile.fullname,
        'lesson'   : lesson,
        'videos' : videos,
        'docs' : docs,
        'images' : images,
        'steps' : steps,
        'texts' : texts,
        })
    return render_to_response('lesson/lesson_view.html',variables)

@login_required
def delete_lesson(request, username, id) :
    lesson = get_object_or_404(Lesson, id = id)
    lesson.delete()
    return HttpResponseRedirect('/user/' + username)

@login_required
def edit_lesson_info(request, username, id) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    lesson = get_object_or_404(Lesson, id = id)
    if request.method == 'POST' :
        form = CreateLesson(request.POST)
        if form.is_valid() :
            lesson.lessonTitle = form.cleaned_data['lessonTitle']
            lesson.gradeLevel = form.cleaned_data['gradeLevel']
            lesson.subject = form.cleaned_data['subject']
            lesson.description = form.cleaned_data['description']
            lesson.save()
            variables = RequestContext ( request,{
                'username' : username,
                'fullname' : user_profile.fullname,
                'lesson'   : lesson
            })
            return render_to_response('lesson/lesson_edit.html', variables)

    form = CreateLesson(initial={
        'lessonTitle' : lesson.lessonTitle,
        'gradeLevel' : lesson.gradeLevel,
        'subject' : lesson.subject,
        'description' : lesson.description
    })
    variables = RequestContext(request,{
        'form' : form,
        'lesson' : lesson,
        'fullname' : user_profile.fullname,
        'username' : username,
        })
    return render_to_response('lesson/lesson_edit_info.html', variables)

@login_required
def add_video(request, username, id) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    lesson = get_object_or_404(Lesson, id = id)
    if request.method == 'POST' :
        form = AddVideoForm(request.POST)
        if form.is_valid() :
            Video.objects.create(
                lesson = lesson,
                pageTitle = form.cleaned_data['pageTitle'],
                url = form.cleaned_data['url'],
                text = form.cleaned_data['text'],
            )
            return HttpResponseRedirect('/user/'+username+'/lesson/'+id+'/edit/')
    else :
        form = AddVideoForm()
    variables = RequestContext(request,{
        'form' : form,
        'fullname' : user_profile.fullname,
        'username' : username,
        })
    return render_to_response('lesson/add_video_page.html',variables)

@login_required
def add_doc(request, username, id ) :
    lesson = get_object_or_404(Lesson, id = id)
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if request.method == 'POST' :
        form = AddDocumentForm(request.POST, request.FILES)
        if form.is_valid() :
            Document.objects.create(
                lesson = lesson,
                file_doc = form.cleaned_data['selectFile'],
                pageTitle = form.cleaned_data['pageTitle'],
                text = form.cleaned_data['text'],
            )
            File_doc.objects.create(
                user = user_profile,
                file = request.FILES['uploadFile']
            )
            return HttpResponseRedirect('/user/'+username+'/lesson/'+id+'/edit/')
    else :
        form = AddDocumentForm()
        file_Upload_Form = FileUploadForm()
    variables = RequestContext(request,{
        'form' : form,
        'fileUploadForm' : file_Upload_Form,
        'fullname' : user_profile.fullname,
        'username' : username,
        })
    return render_to_response('lesson/add_ppdoc_page.html',variables)

@login_required
def add_image(request, username, id) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    lesson = get_object_or_404(Lesson, id = id)
    if request.method == 'POST' :
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid() :
            Image.objects.create(
                lesson = lesson,
                image = form.cleaned_data['selectFile'],
                pageTitle = form.cleaned_data['pageTitle'],
                text = form.cleaned_data['text'],
            )
            File_img.objects.create(
                user = user_profile,
                file = request.FILES['uploadFile']
            )
            return HttpResponseRedirect('/user/'+username+'/lesson/'+id+'/edit/')
    else :
        form = AddImageForm()
        file_Upload_Form = FileUploadForm()
    variables = RequestContext(request,{
        'form' : form,
        'fileUploadForm' : file_Upload_Form,
        'fullname' : user_profile.fullname,
        'username' : username,
        })
    return render_to_response('lesson/add_image_page.html',variables)

@login_required
def add_step(request, username, id) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    lesson = get_object_or_404(Lesson, id = id)
    if request.method == 'POST' :
        form = AddStepbyStepForm(request.POST)
        if form.is_valid() :
            StepbyStep.objects.create(
                lesson = lesson,
                pageTitle = form.cleaned_data['pageTitle'],
                promt = form.cleaned_data['promt'],
                step = form.cleaned_data['step'],
                explain = form.cleaned_data['explain'],
            )
            return HttpResponseRedirect('/user/'+username+'/lesson/'+id+'/edit/')
    else :
        form = AddStepbyStepForm()
    variables = RequestContext(request,{
        'form' : form,
        'fullname' : user_profile.fullname,
        'username' : username,
    })
    return render_to_response('lesson/add_stepbystep_page.html',variables)

@login_required
def add_text(request, username, id) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    lesson = get_object_or_404(Lesson, id = id)
    if request.method == 'POST' :
        form = AddTextForm(request.POST)
        if form.is_valid() :
            Text.objects.create(
                lesson = lesson,
                pageTitle = form.cleaned_data['pageTitle'],
                text = form.cleaned_data['text'],
            )
            return HttpResponseRedirect('/user/'+username+'/lesson/'+id+'/edit/')
    else :
        form = AddTextForm()
    variables = RequestContext(request,{
        'form' : form,
        'fullname' : user_profile.fullname,
        'username' : username,
        })
    return render_to_response('lesson/add_text_page.html',variables)

@login_required
def edit_video(request, username, id_lesson, id_video) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    video = get_object_or_404(Video, id = id_video)
    if request.method == 'POST' :
        form = AddVideoForm(request.POST)
        if form.is_valid() :
            video.pageTitle = form.cleaned_data['pageTitle']
            video.url = form.cleaned_data['url']
            video.text = form.cleaned_data['text']
            video.save()
            return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')

    form = AddVideoForm(initial={
        'pageTitle' : video.pageTitle,
        'url' : video.url,
        'text' : video.text,
    })

    variables = RequestContext(request,{
        'form' : form ,
        'fullname' : user_profile.fullname,
        'username' : username,
    })
    return render_to_response('lesson/add_video_page.html',variables)

@login_required
def edit_doc(request, username, id_lesson , id_doc ) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    doc = get_object_or_404(Document, id = id_doc)
    if request.method == 'POST' :
        form = AddDocumentForm(request.POST)
        if form.is_valid() :
            doc.pageTitle = form.cleaned_data['pageTitle']
            doc.text = form.cleaned_data['text']
            return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')

    form = AddDocumentForm(initial={
        'pageTitle' : video.pageTitle,
        'text' : video.text,
        })

    variables = RequestContext(request,{
        'form' : form,
        'fullname' : user_profile.fullname,
        'username' : username,
    })
    return render_to_response('lesson/add_ppdoc_page.html',variables)

@login_required
def edit_image(request, username, id_lesson, id_image) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    image = get_object_or_404(Image, id = id_image)
    if request.method == 'POST' :
        form = AddImageForm(request.POST)
        if form.is_valid() :
            image.pageTitle = form.cleaned_data['pageTitle']
            image.text = form.cleaned_data['text']
            image.save()
            return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')

    form = AddImageForm(initial={
        'pageTitle' : video.pageTitle,
        'text' : video.text,
        })
    variables = RequestContext(request,{
        'form' : form,
        'fullname' : user_profile.fullname,
        'username' : username,
        })
    return render_to_response('lesson/add_image_page.html',variables)

@login_required
def edit_step(request, username, id_lesson, id_step) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    step = get_object_or_404(StepbyStep, id = id_step)
    if request.method == 'POST' :
        form = AddStepbyStepForm(request.POST)
        if form.is_valid() :
            step.pageTitle = form.cleaned_data['pageTitle']
            step.promt = form.cleaned_data['promt']
            step.save()
            return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')

    form = AddStepbyStepForm(initial={
        'pageTitle' : video.pageTitle,
        'url' : video.url,
        'text' : video.text,
    })

    variables = RequestContext(request,{
        'form' : form,
        'fullname' : user_profile.fullname,
        'username' : username,
    })
    return render_to_response('lesson/add_stepbystep_page.html',variables)

@login_required
def edit_text(request, username, id_lesson, id_text) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    text = get_object_or_404(Text, id = id_text)
    if request.method == 'POST' :
        form = AddTextForm(request.POST)
        if form.is_valid() :
            text.pageTitle = form.cleaned_data['pageTitle']
            text.text = form.cleaned_data['text']
            text.save()
            return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')

    form = AddTextForm(initial={
        'pageTitle' : video.pageTitle,
        'text' : video.text,
    })

    variables = RequestContext(request,{
        'form' : form,
        'fullname' : user_profile.fullname,
        'username' : username,
        })
    return render_to_response('lesson/add_text_page.html',variables)

@login_required
def delete_video(request, username, id_lesson, id_video) :
    video = get_object_or_404(Video, id = id_video)
    video.delete()
    return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')

@login_required
def delete_doc(request, username, id_lesson, id_doc) :
    doc = get_object_or_404(Document, id = id_doc)
    doc.delete()
    return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')

@login_required
def delete_image(request, username, id_lesson, id_image) :
    image = get_object_or_404(Image, id = id_image)
    image.delete()
    return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')

@login_required
def delete_step(request, username, id_lesson, id_step) :
    step = get_object_or_404(StepbyStep, id = id_step)
    step.delete()
    return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')

@login_required
def delete_text(request, username, id_lesson, id_text) :
    text = get_object_or_404(Text, id = id_text)
    text.delete()
    return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')
