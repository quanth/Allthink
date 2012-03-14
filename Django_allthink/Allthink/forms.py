import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import models
from django.forms.fields import ChoiceField
from django.forms.widgets import *

TYPE_USER = ( ('teacher' , 'Teacher'), ('student','Student'))


class LoginForm(forms.Form) :
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='Password (Again)',
        widget=forms.PasswordInput()
    )

    fullname = forms.CharField (label='Your name', max_length=30)

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only containalphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

class CreateLesson(forms.Form) :
    #
    lessonTitle = forms.CharField(label="Lesson title", max_length=100)
    GRADE_LEVEL = (
        ('all','All grade level') ,
        ('e' , 'Elementary') ,
        ('h' , 'High school') ,
        ('c' , 'College')
    )
    gradeLevel = forms.ChoiceField(label="Grade level", widget= Select, choices= GRADE_LEVEL)
    SUBJECT = (
        ('math', 'Math'),
        ('science', 'Science'),
        ('physic', 'Physic')
    )
    subject = forms.ChoiceField(label="Subject", widget= Select  , choices = SUBJECT)
    description = forms.CharField(label="description", widget= Textarea(attrs={'cols': 70, 'rows': 5, 'style' : 'resize: none;'}), max_length=1000)


class AddVideoForm(forms.Form):
    pageTitle = forms.CharField(label= 'pageTitle', max_length=100)
    url = forms.URLField(label='url')
    text = forms.CharField(label="text", widget= Textarea(attrs={'cols': 70, 'rows': 5, 'style' : 'resize: none;'}), max_length=1000)


class AddDocumentForm(forms.Form):
    pageTitle = forms.CharField(label= 'pageTitle', max_length=100)
    #file = models.FileField()
    text = forms.CharField(label="text", widget= Textarea(attrs={'cols': 70, 'rows': 5, 'style' : 'resize: none;'}), max_length=1000)


class AddImageForm(forms.Form):
    pageTitle = forms.CharField(label= 'pageTitle', max_length=100)
    #image = models.ImageField()
    text = forms.CharField(label="text", widget= Textarea(attrs={'cols': 70, 'rows': 5, 'style' : 'resize: none;'}), max_length=1000)


class AddStepbyStepForm(forms.Form):
    pageTitle = forms.CharField(label= 'pageTitle', max_length=100)
    promt = forms.CharField(label= 'promt', widget= Textarea(attrs={'cols': 65, 'rows': 4, 'style' : 'resize: none;'}), max_length=300)


class AddTextForm(forms.Form):
    pageTitle = forms.CharField(label= 'pageTitle', max_length=100)
    text = forms.CharField(label="text", widget= Textarea(attrs={'cols': 70, 'rows': 5, 'style' : 'resize: none;'}), max_length=1000)