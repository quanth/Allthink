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
    lessonTile = forms.CharField(label="Lesson title", max_length=100)
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
    description = forms.CharField(max_length=1000)
