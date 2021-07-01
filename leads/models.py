from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass


class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey("Agent",on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Agent(models.Model):
    user = models.OneToOneField(User,related_name='agent',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email





