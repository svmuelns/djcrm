# We represent data structure of our web page in models.py
# Basically, our database django representation
# Most of the changes here will need a makemigrate, migrate
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_organizer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL) # we link every lead to a category
        # we link a table to another table database
        # we link agent variable to agent model
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # we already have # first_name = models.CharField(max_length=20) # last_name = models.CharField(max_length=20) in AbstractUser
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE) # will allows us to use multiple users to link to the same organization

    def __str__(self):          # this code will output our email
        return self.user.username  # when we Agent.objects.all()
        # return self.user.email

class Category(models.Model): # New, Contacted, Converted, Unconverted
    name = models.CharField(max_length=30)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE) # will allows us to use multiple users to link to the same organization

    
    def __str__(self): # returns name when called function
        return self.name



def post_user_created_signal(sender, instance, created, **kwargs):
    print(instance, created)
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)
# once we create a user or we save changes in that user,
# django will send out the post_save signal
# saying that we want to use that function post_user_created_signal
# that will save a UserProfile anchored to our Django User












# =================== NOTES ====================

# WHAT ARE MODELS ?????

# A model is the single, definitive source of information 
# about your data. It contains the essential fields and 
# behaviors of the data you're storing

# AFTER CREATE MY MODELS, WHAT DO I DO????

# Once you have defined your models, you need to tell Django
# you’re going to use those models. Do this by editing your 
# settings file and changing the INSTALLED_APPS setting to 
# add the name of the module that contains your models.py.

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