from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

import uuid



EXPIRES=(
    ('NEVER','Never'),
    ('10 MIN','10 min'),
    ('1 HR','1 hr'),
    ('1 WEEK','1 week'),
    ('2 WEEK','2 week'),
    ('1 MONTH','1 month'),
    ('6 MONTH','6 month'),
    ('1 YEAR','1 year')
)

LANGUAGE=(
    ('PLAINTEXT', 'PLAINTEXT'),
    ('PYTHON', 'PYTHON'),
    ('JAVASCRIPT', 'JAVASCRIPT'),
    ('GOLANG', 'GOLANG'),
    ('RUBY', 'RUBY'),
    ('HTML', 'HTML'),
    ('JAVA', 'JAVA'),
    ('JSON', 'JSON'),
    ('CSS', 'CSS'),
    ('C#', 'C#'),
    ('C++', 'C++')
)

class CodePaste(models.Model):
    

    paste_uuid=models.UUIDField(default=uuid.uuid4, editable=False)
    title=models.CharField(blank=True,null=True, max_length=500)
    code=models.TextField()
    user =models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    public=models.BooleanField(default=True)
    expiration=models.CharField(choices=EXPIRES, max_length=30,default='NEVER')
    language=models.CharField(choices=LANGUAGE, default='PLAINTEXT', max_length=30)
    syntax_highlighting=models.BooleanField(default=False)
    password=models.CharField(blank=True,null=True, max_length=300)
    folder=models.ForeignKey('CodeFolder',on_delete=models.CASCADE,null=True,blank=True)
    views=models.IntegerField(default=0)

    def save(self,*args, **kwargs):
        if not self.title:
            self.title="Untitled"
        if not self.password:
            self.password=None

        return super().save(*args, **kwargs)


class CodeFolder(models.Model):
    name=models.CharField(max_length=500)
    user =models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    folder_uuid=models.UUIDField(default=uuid.uuid4, editable=False)
    

class UserProfile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    website_url=models.URLField(max_length=225,null=True,blank=True)
    location=models.CharField(max_length=225,blank=True,null=True)
    avatar=models.ImageField(blank=True,null=True,upload_to='profile_images')

    def get_avatar_url(self):
        return settings.BASE_URL + self.avatar.url


class UserSettings(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    defaultSyntax=models.CharField(choices=LANGUAGE,max_length=30,default='PLAINTEXT')
    defaultExpiration=models.CharField(choices=EXPIRES, max_length=30,default='NEVER')
    nightMode=models.BooleanField(default=True)
    defaultExposure=models.BooleanField(default=True)


# class PasteBinProfile(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
#     number_of_pr

def setup_user(sender,instance,created,*args, **kwargs):
    if created:
        UserSettings.objects.create(user=instance)
        UserProfile.objects.create(user=instance)
        

post_save.connect(setup_user,sender=User)