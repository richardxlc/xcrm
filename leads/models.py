from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_organizor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    organization = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent",on_delete=models.SET_NULL,null=True,blank=True)
    category = models.ForeignKey("Category",related_name="leads", on_delete=models.SET_NULL,null=True,blank=True)
    description = models.TextField()
    phone_number = models.CharField(max_length=20)
    date_add = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    #Lead.objects.filter(category=category)
    #category.lead_set.all()
    #category.leads.all()


class Agent(models.Model):
    user = models.OneToOneField(User,related_name='agent',on_delete=models.CASCADE)
    organization = models.ForeignKey(UserProfile,on_delete=models.CASCADE)


    def __str__(self):
        return self.user.email

class Category(models.Model):
    name = models.CharField(max_length=30) # 新建，已联系，已转化，未转化
    organization = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

def post_user_create_signal(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_create_signal,sender=User)





