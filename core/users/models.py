from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
# Create your models here.


class User(AbstractUser):
    is_freelancer=models.BooleanField(default=False)
    is_client=models.BooleanField(default=False)

    def __str__(self):
        return self.username

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)


class Freelancer(models.Model):
    user=models.OneToOneField(User, related_name="freelancer",on_delete=models.CASCADE)
    phone=models.CharField(max_length=200,blank=True)
    skill=models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.user.username


class Client(models.Model):
    user=models.OneToOneField(User, related_name="employer",on_delete=models.CASCADE)
    company_name=models.CharField(max_length=200,blank=True)
    description=models.TextField(null=True)

    def __str__(self):
        return self.company_name
