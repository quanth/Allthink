import re
from django.contrib.auth.models import  User
from django.db import models
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='user_profile')
    typeUser = models.CharField(max_length=20)
    fullname = models.CharField(max_length=30)

#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        UserProfile.objects.create(user=instance)
#
#post_save.connect(create_user_profile, sender=User)

class Lesson(models.Model):
    user = models.ForeignKey(UserProfile, related_name='lesson')
    #
    lessonTitle = models.CharField(max_length=100)
    GRADE_LEVEL = (
        ('all','All grade level') ,
        ('e' , 'Elementary') ,
        ('h' , 'High school') ,
        ('c' , 'College')
    )
    gradeLevel = models.CharField(max_length=30, choices= GRADE_LEVEL)
    SUBJECT = (
        ('math', 'Math'),
        ('science', 'Science'),
        ('physic', 'Physic')
    )
    subject = models.CharField(max_length=30, choices = SUBJECT)
    description = models.TextField(max_length=1000)

class Video(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='lesson_video')
    pageTitle = models.CharField(max_length=100)
    url = models.URLField()
    text = models.TextField(max_length=1000)
    def youtube(self):
        regex = re.compile(r"^(http://)?(www\.)?(youtube\.com/watch\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})")
        match = regex.match(self.url)
        if not match: return ""
        video_id = match.group('id')
        return video_id


class Document(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='lesson_doc')
    file_doc = models.CharField(max_length=10)
    pageTitle = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)


class Image(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='lesson_image')
    pageTitle = models.CharField(max_length=100)
    image = models.CharField(max_length=10)
    text = models.TextField(max_length=1000)


class StepbyStep(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='lesson_step')
    pageTitle = models.CharField(max_length=100)
    promt = models.CharField(max_length=300)
    step = models.CharField(max_length=100)
    explain = models.CharField(max_length=100)

class Text(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='lesson_text')
    pageTitle = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)

class File_doc(models.Model) :
    user = models.ForeignKey(UserProfile, related_name='file_doc')
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to= 'DB/documents')

class File_img(models.Model) :
    user = models.ForeignKey(UserProfile, related_name='file_img')
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to= 'DB/images')
