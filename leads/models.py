# We represent data structure of our web page in models.py

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE) 
        # we link a table to another table database
        # we link agent variable to agent model
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # we already have # first_name = models.CharField(max_length=20) # last_name = models.CharField(max_length=20) in AbstractUser

    def __str__(self):          # this code will output our email
        return self.user.email  # when we Agent.objects.all()

# =================== NOTES ====================

    #phoned = models.BooleanField(default=False)
    #source = models.CharField(choices = SOURCE_CHOICES, max_length=100)

    #profile_picture = models.ImageField(blank=True, null=True) # submitting a empty value, no value in database
    #special_files = models.FileField(blank=True, null=True)




    #SOURCE_CHOICES = (
    #    ('YouTube', 'YouTube'), # database value, display value
    #    ('Google', 'Google'),
    #    ('Newsletter', 'Newsletter'),
    #)


        # ForeignKeys need 'on_delete' so we know what will hapen if
        # we delete that Agent
        # .CASCADE      if the Agent is deleted, delete the lead
        # .SET_NULL, null=True
        # .SET_DEFAULT, null=True, default=  