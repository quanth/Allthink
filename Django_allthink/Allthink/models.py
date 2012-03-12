from django.contrib.auth.models import  User
from django.db import models
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    typeUser = models.CharField(max_length=20)
    fullname = models.CharField(max_length=30)

#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        UserProfile.objects.create(user=instance)
#
#post_save.connect(create_user_profile, sender=User)

class Video(models.Model):
    pageTile = models.CharField(max_length=100)
    url = models.URLField()
    text = models.CharField(max_length=1000)


class Document(models.Model):
    pageTile = models.CharField(max_length=100)
    #file = models.FileField()
    text = models.CharField(max_length=1000)


class Image(models.Model):
    pageTile = models.CharField(max_length=100)
    #image = models.ImageField()
    text = models.CharField(max_length=1000)


class StepbyStep(models.Model):
    pageTile = models.CharField(max_length=100)
    promt = models.CharField(max_length=100)


class Text(models.Model):
    pageTile = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)


class Lesson(models.Model):
    user = models.ForeignKey(UserProfile)
    #
    lessonTile = models.CharField(max_length=100)
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
    description = models.CharField(max_length=1000)
    #
    video = models.ForeignKey(Video)
    document = models.ForeignKey(Document)
    image = models.ForeignKey(Image)
    stepbystep = models.ForeignKey(StepbyStep)
    text = models.ForeignKey(Text)
